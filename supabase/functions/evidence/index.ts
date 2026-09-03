import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
const allowedOrigin = Deno.env.get("ALLOWED_ORIGIN") ?? "*";
const admin = createClient(supabaseUrl, serviceRoleKey, {
  auth: { persistSession: false, autoRefreshToken: false },
});

const cors = {
  "Access-Control-Allow-Origin": allowedOrigin,
  "Access-Control-Allow-Headers": "apikey, authorization, content-type, x-access-code",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
};

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

function cleanName(name: string): string {
  return name.toLowerCase().replace(/[^a-z0-9._-]+/g, "-").slice(-80) || "evidence";
}

Deno.serve(async (request) => {
  if (request.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (!supabaseUrl || !serviceRoleKey) return json({ error: "Evidence service is not configured" }, 500);

  const code = request.headers.get("x-access-code")?.trim() ?? "";
  if (code.length < 20) return json({ error: "Access denied" }, 403);

  if (request.method === "GET") {
    const path = new URL(request.url).searchParams.get("path") ?? "";
    if (!path || path.includes("..")) return json({ error: "Invalid evidence path" }, 400);
    const { data: allowed, error: accessError } = await admin.rpc("can_access_evidence", {
      p_code: code,
      p_path: path,
    });
    if (accessError || !allowed) return json({ error: "Access denied" }, 403);
    const { data, error } = await admin.storage.from("test-evidence").createSignedUrl(path, 300);
    if (error) return json({ error: "Screenshot could not be opened" }, 404);
    return json({ url: data.signedUrl, expiresIn: 300 });
  }

  if (request.method !== "POST") return json({ error: "Method not allowed" }, 405);
  const form = await request.formData().catch(() => null);
  const file = form?.get("file");
  const runId = String(form?.get("runId") ?? "");
  const testId = String(form?.get("testId") ?? "");
  if (!(file instanceof File) || !runId || !/^[A-Z]\d{2}$/.test(testId)) {
    return json({ error: "File, run, or test details are missing" }, 400);
  }
  const allowedTypes = new Set(["image/png", "image/jpeg", "image/webp"]);
  if (!allowedTypes.has(file.type)) return json({ error: "Use a PNG, JPEG, or WebP image" }, 400);
  if (file.size > 5 * 1024 * 1024) return json({ error: "Screenshot must be 5 MiB or smaller" }, 400);

  const { data: testerId, error: testerError } = await admin.rpc("resolve_tester_upload", {
    p_code: code,
    p_run_id: runId,
    p_test_id: testId,
  });
  if (testerError || !testerId) return json({ error: "Upload access denied" }, 403);

  const path = `${testerId}/${runId}/${testId}-${Date.now()}-${cleanName(file.name)}`;
  const { error: uploadError } = await admin.storage.from("test-evidence").upload(path, file, {
    contentType: file.type,
    cacheControl: "3600",
    upsert: false,
  });
  if (uploadError) return json({ error: "Screenshot upload failed" }, 500);
  return json({ path }, 201);
});
