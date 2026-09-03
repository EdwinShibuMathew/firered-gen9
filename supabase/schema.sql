-- FireRed Gen 9 testing dashboard schema.
-- Apply this file first, then supabase/seed.sql, in the Supabase SQL editor.

create extension if not exists pgcrypto;

create table if not exists public.checklist_items (
    checklist_version text not null,
    test_id text not null,
    section text not null,
    instruction text not null,
    expected text not null,
    display_order integer not null,
    primary key (checklist_version, test_id)
);

create table if not exists public.testers (
    id uuid primary key default gen_random_uuid(),
    display_name text not null unique,
    code_hash text not null unique,
    active boolean not null default true,
    created_at timestamptz not null default now()
);

create table if not exists public.admin_access (
    singleton boolean primary key default true check (singleton),
    code_hash text not null,
    updated_at timestamptz not null default now()
);

create table if not exists public.test_runs (
    id uuid primary key default gen_random_uuid(),
    tester_id uuid not null references public.testers(id) on delete cascade,
    checklist_version text not null,
    profile jsonb not null default '{}'::jsonb,
    active boolean not null default true,
    started_at timestamptz not null default now(),
    completed_at timestamptz,
    updated_at timestamptz not null default now()
);

create unique index if not exists one_active_run_per_version
    on public.test_runs (tester_id, checklist_version) where active;

create table if not exists public.test_results (
    run_id uuid not null references public.test_runs(id) on delete cascade,
    checklist_version text not null,
    test_id text not null,
    status text not null check (status in ('not_started', 'passed', 'failed', 'skipped')),
    notes text not null default '' check (length(notes) <= 5000),
    evidence_path text,
    updated_at timestamptz not null default now(),
    primary key (run_id, test_id),
    foreign key (checklist_version, test_id)
        references public.checklist_items(checklist_version, test_id)
);

alter table public.checklist_items enable row level security;
alter table public.testers enable row level security;
alter table public.admin_access enable row level security;
alter table public.test_runs enable row level security;
alter table public.test_results enable row level security;

revoke all on public.checklist_items from anon, authenticated;
revoke all on public.testers from anon, authenticated;
revoke all on public.admin_access from anon, authenticated;
revoke all on public.test_runs from anon, authenticated;
revoke all on public.test_results from anon, authenticated;

create or replace function public.configure_test_access(
    p_tester_one_name text,
    p_tester_one_code text,
    p_tester_two_name text,
    p_tester_two_code text,
    p_admin_code text
) returns void
language plpgsql
security definer set search_path = ''
as $$
begin
    if least(length(p_tester_one_code), length(p_tester_two_code), length(p_admin_code)) < 20 then
        raise exception 'Access codes must contain at least 20 characters';
    end if;
    insert into public.testers (display_name, code_hash)
    values (p_tester_one_name, extensions.crypt(p_tester_one_code, extensions.gen_salt('bf', 12)))
    on conflict (display_name) do update
       set code_hash = excluded.code_hash, active = true;
    insert into public.testers (display_name, code_hash)
    values (p_tester_two_name, extensions.crypt(p_tester_two_code, extensions.gen_salt('bf', 12)))
    on conflict (display_name) do update
       set code_hash = excluded.code_hash, active = true;
    insert into public.admin_access (singleton, code_hash)
    values (true, extensions.crypt(p_admin_code, extensions.gen_salt('bf', 12)))
    on conflict (singleton) do update
       set code_hash = excluded.code_hash, updated_at = now();
end;
$$;

create or replace function public.tester_session(p_code text, p_checklist_version text)
returns jsonb
language plpgsql
security definer set search_path = ''
as $$
declare
    selected_tester public.testers%rowtype;
    selected_run public.test_runs%rowtype;
    result_rows jsonb;
begin
    select * into selected_tester
      from public.testers
     where active and extensions.crypt(p_code, code_hash) = code_hash
     for update;
    if selected_tester.id is null then raise exception 'Code not recognised'; end if;
    if not exists (
        select 1 from public.checklist_items where checklist_version = p_checklist_version
    ) then raise exception 'Checklist version is not installed'; end if;

    select * into selected_run
      from public.test_runs
     where tester_id = selected_tester.id
       and checklist_version = p_checklist_version
       and active
     order by started_at desc limit 1;
    if selected_run.id is null then
        insert into public.test_runs (tester_id, checklist_version)
        values (selected_tester.id, p_checklist_version)
        returning * into selected_run;
    end if;

    select coalesce(jsonb_agg(to_jsonb(r) order by r.test_id), '[]'::jsonb)
      into result_rows
      from public.test_results r where r.run_id = selected_run.id;
    return jsonb_build_object(
        'role', 'tester',
        'tester', jsonb_build_object('id', selected_tester.id, 'display_name', selected_tester.display_name),
        'run', to_jsonb(selected_run),
        'results', result_rows
    );
end;
$$;

create or replace function public.save_test_result(
    p_code text,
    p_run_id uuid,
    p_test_id text,
    p_status text,
    p_notes text,
    p_evidence_path text default null
) returns void
language plpgsql
security definer set search_path = ''
as $$
declare
    selected_tester uuid;
    selected_version text;
begin
    select id into selected_tester from public.testers
     where active and extensions.crypt(p_code, code_hash) = code_hash;
    if selected_tester is null then raise exception 'Code not recognised'; end if;
    select checklist_version into selected_version from public.test_runs
     where id = p_run_id and tester_id = selected_tester and active;
    if selected_version is null then raise exception 'Testing run not found'; end if;
    if p_status not in ('not_started', 'passed', 'failed', 'skipped') then
        raise exception 'Invalid status';
    end if;
    if length(coalesce(p_notes, '')) > 5000 then raise exception 'Notes are too long'; end if;
    if p_evidence_path is not null and p_evidence_path !~ ('^' || selected_tester::text || '/' || p_run_id::text || '/') then
        raise exception 'Evidence path does not belong to this run';
    end if;

    insert into public.test_results
        (run_id, checklist_version, test_id, status, notes, evidence_path, updated_at)
    values
        (p_run_id, selected_version, p_test_id, p_status, coalesce(p_notes, ''), p_evidence_path, now())
    on conflict (run_id, test_id) do update set
        status = excluded.status,
        notes = excluded.notes,
        evidence_path = excluded.evidence_path,
        updated_at = now();
    update public.test_runs set updated_at = now() where id = p_run_id;
end;
$$;

create or replace function public.save_run_profile(
    p_code text,
    p_run_id uuid,
    p_profile jsonb
) returns void
language plpgsql
security definer set search_path = ''
as $$
declare selected_tester uuid;
begin
    select id into selected_tester from public.testers
     where active and extensions.crypt(p_code, code_hash) = code_hash;
    if selected_tester is null then raise exception 'Code not recognised'; end if;
    update public.test_runs
       set profile = jsonb_strip_nulls(p_profile), updated_at = now()
     where id = p_run_id and tester_id = selected_tester and active;
    if not found then raise exception 'Testing run not found'; end if;
end;
$$;

create or replace function public.admin_dashboard(p_code text)
returns jsonb
language plpgsql
security definer set search_path = ''
as $$
declare tester_rows jsonb; result_rows jsonb;
begin
    if not exists (
        select 1 from public.admin_access where singleton and extensions.crypt(p_code, code_hash) = code_hash
    ) then raise exception 'Administrator access denied'; end if;

    select coalesce(jsonb_agg(to_jsonb(summary) order by summary.display_name), '[]'::jsonb)
      into tester_rows
      from (
        select t.id, t.display_name, r.id as run_id, r.checklist_version, r.profile,
               count(tr.test_id) filter (where tr.status <> 'not_started')::int as completed,
               count(tr.test_id) filter (where tr.status = 'passed')::int as passed,
               count(tr.test_id) filter (where tr.status = 'failed')::int as failed,
               count(tr.test_id) filter (where tr.status = 'skipped')::int as skipped,
               greatest(count(ci.test_id) - count(tr.test_id) filter (where tr.status <> 'not_started'), 0)::int as not_started,
               r.updated_at
          from public.testers t
          left join lateral (
              select * from public.test_runs rr where rr.tester_id = t.id and rr.active
              order by rr.started_at desc limit 1
          ) r on true
          left join public.checklist_items ci on ci.checklist_version = r.checklist_version
          left join public.test_results tr on tr.run_id = r.id and tr.test_id = ci.test_id
         where t.active
         group by t.id, t.display_name, r.id, r.checklist_version, r.profile, r.updated_at
      ) summary;

    select coalesce(jsonb_agg(to_jsonb(detail) order by detail.tester_name, detail.test_id), '[]'::jsonb)
      into result_rows
      from (
        select t.display_name as tester_name, r.id as run_id, tr.test_id, tr.status,
               tr.notes, tr.evidence_path, tr.updated_at
          from public.test_results tr
          join public.test_runs r on r.id = tr.run_id and r.active
          join public.testers t on t.id = r.tester_id and t.active
      ) detail;
    return jsonb_build_object('role', 'admin', 'testers', tester_rows, 'results', result_rows);
end;
$$;

create or replace function public.resolve_tester_upload(p_code text, p_run_id uuid, p_test_id text)
returns uuid
language plpgsql
security definer set search_path = ''
as $$
declare selected_tester uuid;
begin
    select t.id into selected_tester
      from public.testers t
      join public.test_runs r on r.tester_id = t.id
     where t.active and r.active and r.id = p_run_id
       and extensions.crypt(p_code, t.code_hash) = t.code_hash
       and exists (
           select 1 from public.checklist_items ci
            where ci.checklist_version = r.checklist_version and ci.test_id = p_test_id
       );
    if selected_tester is null then raise exception 'Upload access denied'; end if;
    return selected_tester;
end;
$$;

create or replace function public.can_access_evidence(p_code text, p_path text)
returns boolean
language plpgsql
security definer set search_path = ''
as $$
declare selected_tester uuid;
begin
    if exists (select 1 from public.admin_access where singleton and extensions.crypt(p_code, code_hash) = code_hash) then
        return true;
    end if;
    select id into selected_tester from public.testers
     where active and extensions.crypt(p_code, code_hash) = code_hash;
    return selected_tester is not null and p_path like selected_tester::text || '/%';
end;
$$;

create or replace function public.start_new_test_run(p_admin_code text, p_tester_id uuid, p_checklist_version text)
returns uuid
language plpgsql
security definer set search_path = ''
as $$
declare new_id uuid;
begin
    if not exists (
        select 1 from public.admin_access where singleton and extensions.crypt(p_admin_code, code_hash) = code_hash
    ) then raise exception 'Administrator access denied'; end if;
    update public.test_runs set active = false, completed_at = now()
     where tester_id = p_tester_id and checklist_version = p_checklist_version and active;
    insert into public.test_runs (tester_id, checklist_version)
    values (p_tester_id, p_checklist_version) returning id into new_id;
    return new_id;
end;
$$;

revoke execute on function public.configure_test_access(text, text, text, text, text) from public, anon, authenticated;
revoke execute on function public.resolve_tester_upload(text, uuid, text) from public, anon, authenticated;
revoke execute on function public.can_access_evidence(text, text) from public, anon, authenticated;
grant execute on function public.resolve_tester_upload(text, uuid, text) to service_role;
grant execute on function public.can_access_evidence(text, text) to service_role;

revoke execute on function public.tester_session(text, text) from public, authenticated;
revoke execute on function public.save_test_result(text, uuid, text, text, text, text) from public, authenticated;
revoke execute on function public.save_run_profile(text, uuid, jsonb) from public, authenticated;
revoke execute on function public.admin_dashboard(text) from public, authenticated;
revoke execute on function public.start_new_test_run(text, uuid, text) from public, authenticated;
grant execute on function public.tester_session(text, text) to anon;
grant execute on function public.save_test_result(text, uuid, text, text, text, text) to anon;
grant execute on function public.save_run_profile(text, uuid, jsonb) to anon;
grant execute on function public.admin_dashboard(text) to anon;
grant execute on function public.start_new_test_run(text, uuid, text) to anon;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('test-evidence', 'test-evidence', false, 5242880, array['image/png', 'image/jpeg', 'image/webp'])
on conflict (id) do update set
    public = false,
    file_size_limit = excluded.file_size_limit,
    allowed_mime_types = excluded.allowed_mime_types;

-- The bucket has no anon/authenticated storage policies. Evidence is available
-- only through the validated Edge Function using its server-side service role.
