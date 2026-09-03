# Testing Dashboard Setup

The dashboard in `test-dashboard/` is a static GitHub Pages site backed by Supabase. Testers use private codes; the administrator code opens the combined live dashboard.

**Live dashboard:** <https://edwinshibumathew.github.io/firered-gen9/>

The GBA ROM, save files, access codes, uploaded screenshots, and Supabase service-role key must never be committed or published through GitHub Pages.

## 1. Create the Supabase backend

1. Create a Supabase project.
2. Open **SQL Editor** in the project dashboard.
3. Run `supabase/schema.sql`.
4. Run `supabase/seed.sql`.
5. Generate three independent codes of at least 20 characters. A password manager is recommended.
6. In SQL Editor, replace the example values and run:

```sql
select public.configure_test_access(
  'Tester 1', 'REPLACE_WITH_FIRST_PRIVATE_CODE',
  'Tester 2', 'REPLACE_WITH_SECOND_PRIVATE_CODE',
  'REPLACE_WITH_ADMIN_PRIVATE_CODE'
);
```

The codes are salted and hashed by PostgreSQL. Save the original codes in a password manager because they cannot be recovered from the database.

## 2. Deploy the screenshot function

Install the Supabase CLI and link this repository to the project:

```sh
supabase login
supabase link --project-ref YOUR_PROJECT_REF
supabase secrets set ALLOWED_ORIGIN=https://edwinshibumathew.github.io
supabase functions deploy evidence --no-verify-jwt
```

If the Pages site uses a custom domain, use that exact origin instead. The function validates private codes before accepting an upload or returning a five-minute screenshot URL. PNG, JPEG, and WebP files up to 5 MiB are accepted.

## 3. Configure GitHub Pages

In the GitHub repository, open **Settings > Secrets and variables > Actions > Variables** and add:

- `SUPABASE_URL` — the project URL from **Supabase > Project Settings > API**.
- `SUPABASE_PUBLISHABLE_KEY` — the publishable key from the same page. Older projects may call it the anon key.

Never use the secret key or service-role key in GitHub Pages variables.

Then open **Settings > Pages** and select **GitHub Actions** as the source. Push the dashboard files to `main`, or run **Deploy testing dashboard** from the Actions tab. The workflow validates the generated checklist and publishes only the static dashboard files.

## 4. Share and use the dashboard

1. Open the deployed Pages URL.
2. Test the administrator code and verify that the combined dashboard opens.
3. Send each tester the Pages URL and only their own private tester code.
4. Ask each tester to enter setup details before starting.
5. Use the administrator dashboard to review progress, failures, notes, screenshots, and exports.

Codes are intentionally not embedded in URLs, screenshots, or repository files.

## Updating the checklist

Edit `docs/FULL_PLAYTHROUGH_TEST_PLAN.md`, then run:

```sh
python3 scripts/generate_test_dashboard_data.py
python3 scripts/generate_test_dashboard_data.py --check
```

Apply the updated `supabase/seed.sql` before deploying the frontend. The checklist version changes with its Markdown content, so existing historical test runs remain intact and each tester receives a fresh run for the new version.

## Starting another run of the same checklist

Look up the tester UUID in Supabase's `testers` table, then call:

```sql
select public.start_new_test_run(
  'YOUR_ADMIN_PRIVATE_CODE',
  'TESTER_UUID',
  'CHECKLIST_VERSION_FROM_test-dashboard/checklist.json'
);
```

The earlier run remains stored but becomes inactive.

## Local checks

```sh
python3 scripts/generate_test_dashboard_data.py --check
python3 -m http.server 8080 --directory test-dashboard
```

The checked-in `config.js` contains only the browser-safe project URL and publishable key. It never contains the secret or service-role key.
