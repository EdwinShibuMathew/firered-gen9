"use strict";

const config = window.TEST_DASHBOARD_CONFIG || {};
const $ = (selector) => document.querySelector(selector);
const state = {
  checklist: null,
  code: localStorage.getItem("firered-test-code") || "",
  session: null,
  results: new Map(),
  adminData: null,
  noteTimers: new Map(),
};

function configured() {
  return Boolean(config.supabaseUrl && config.supabasePublishableKey);
}

function show(view) {
  ["loginView", "testerView", "adminView"].forEach((id) => $("#" + id).classList.toggle("hidden", id !== view));
  $("#logoutButton").classList.toggle("hidden", view === "loginView");
}

function message(element, text, kind = "") {
  element.textContent = text;
  element.className = "message" + (kind ? " " + kind : "");
}

async function rpc(name, args) {
  const response = await fetch(`${config.supabaseUrl}/rest/v1/rpc/${name}`, {
    method: "POST",
    headers: {
      apikey: config.supabasePublishableKey,
      Authorization: `Bearer ${config.supabasePublishableKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(args),
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) throw new Error(data?.message || data?.error || "Request failed");
  return data;
}

async function loadChecklist() {
  const response = await fetch("checklist.json", { cache: "no-store" });
  if (!response.ok) throw new Error("Could not load the checklist");
  state.checklist = await response.json();
}

function resultFor(testId) {
  return state.results.get(testId) || { test_id: testId, status: "not_started", notes: "", evidence_path: null };
}

function pendingKey() {
  return `firered-pending-${state.session?.run?.id || "none"}`;
}

function queuePending(result) {
  const pending = JSON.parse(localStorage.getItem(pendingKey()) || "{}");
  pending[result.test_id] = result;
  localStorage.setItem(pendingKey(), JSON.stringify(pending));
}

function clearPending(testId) {
  const pending = JSON.parse(localStorage.getItem(pendingKey()) || "{}");
  delete pending[testId];
  localStorage.setItem(pendingKey(), JSON.stringify(pending));
}

async function saveResult(result, card) {
  state.results.set(result.test_id, result);
  queuePending(result);
  updateProgress();
  setCardStatus(card, result.status);
  message(card.querySelector(".card-message"), "Saving…");
  try {
    await rpc("save_test_result", {
      p_code: state.code,
      p_run_id: state.session.run.id,
      p_test_id: result.test_id,
      p_status: result.status,
      p_notes: result.notes || "",
      p_evidence_path: result.evidence_path || null,
    });
    clearPending(result.test_id);
    message(card.querySelector(".card-message"), "Saved", "success");
    message($("#syncMessage"), "All changes saved", "success");
  } catch (error) {
    message(card.querySelector(".card-message"), "Saved on this device; waiting to sync", "error");
    message($("#syncMessage"), "Some changes are waiting to sync", "error");
  }
}

async function retryPending() {
  const pending = JSON.parse(localStorage.getItem(pendingKey()) || "{}");
  const entries = Object.values(pending);
  if (!entries.length) {
    message($("#syncMessage"), "Everything is already saved", "success");
    return;
  }
  message($("#syncMessage"), `Syncing ${entries.length} change(s)…`);
  for (const result of entries) {
    await rpc("save_test_result", {
      p_code: state.code,
      p_run_id: state.session.run.id,
      p_test_id: result.test_id,
      p_status: result.status,
      p_notes: result.notes || "",
      p_evidence_path: result.evidence_path || null,
    });
    clearPending(result.test_id);
  }
  message($("#syncMessage"), "All changes saved", "success");
}

function setCardStatus(card, status) {
  card.dataset.status = status;
  card.querySelectorAll("[data-status]").forEach((button) => button.classList.toggle("active", button.dataset.status === status));
}

function createCard(item) {
  const card = $("#testCardTemplate").content.firstElementChild.cloneNode(true);
  const result = resultFor(item.id);
  card.dataset.testId = item.id;
  card.querySelector(".test-id").textContent = item.id;
  card.querySelector(".instruction").textContent = item.instruction;
  card.querySelector(".expected").textContent = item.expected;
  card.querySelector("textarea").value = result.notes || "";
  setCardStatus(card, result.status);
  if (result.evidence_path) {
    card.querySelector(".evidence-name").textContent = "Screenshot attached";
    card.querySelector(".view-evidence").classList.remove("hidden");
  }
  card.querySelectorAll("[data-status]").forEach((button) => button.addEventListener("click", () => {
    const next = { ...resultFor(item.id), status: button.dataset.status };
    saveResult(next, card);
  }));
  card.querySelector("textarea").addEventListener("input", (event) => {
    clearTimeout(state.noteTimers.get(item.id));
    state.noteTimers.set(item.id, setTimeout(() => {
      const next = { ...resultFor(item.id), notes: event.target.value.trim() };
      saveResult(next, card);
    }, 700));
  });
  card.querySelector(".evidence-input").addEventListener("change", (event) => uploadEvidence(item.id, event.target.files[0], card));
  card.querySelector(".view-evidence").addEventListener("click", () => viewEvidence(resultFor(item.id).evidence_path));
  return card;
}

function renderChecklist() {
  const host = $("#checklist");
  host.replaceChildren();
  const groups = new Map();
  for (const item of state.checklist.items) {
    if (!groups.has(item.section)) groups.set(item.section, []);
    groups.get(item.section).push(item);
  }
  for (const [sectionName, items] of groups) {
    const details = document.createElement("details");
    details.className = "section";
    details.open = true;
    const summary = document.createElement("summary");
    const name = document.createElement("span");
    name.textContent = sectionName;
    const count = document.createElement("span");
    count.className = "section-count";
    count.dataset.section = sectionName;
    summary.append(name, count);
    details.append(summary, ...items.map(createCard));
    host.append(details);
  }
  applyFilters();
  updateProgress();
}

function updateProgress() {
  if (!state.checklist) return;
  const completed = [...state.results.values()].filter((row) => row.status !== "not_started").length;
  $("#progressText").textContent = `${completed} / ${state.checklist.count} reviewed`;
  $("#progressBar").style.width = `${completed / state.checklist.count * 100}%`;
  document.querySelectorAll(".section-count").forEach((node) => {
    const items = state.checklist.items.filter((item) => item.section === node.dataset.section);
    const done = items.filter((item) => resultFor(item.id).status !== "not_started").length;
    node.textContent = `${done} / ${items.length}`;
  });
}

function applyFilters() {
  const wanted = $("#statusFilter").value;
  const query = $("#searchInput").value.trim().toLowerCase();
  document.querySelectorAll(".test-card").forEach((card) => {
    const item = state.checklist.items.find((entry) => entry.id === card.dataset.testId);
    const matchesStatus = wanted === "all" || resultFor(item.id).status === wanted;
    const haystack = `${item.id} ${item.instruction} ${item.expected}`.toLowerCase();
    card.classList.toggle("hidden", !matchesStatus || !haystack.includes(query));
  });
}

async function uploadEvidence(testId, file, card) {
  if (!file) return;
  const allowed = ["image/png", "image/jpeg", "image/webp"];
  if (!allowed.includes(file.type) || file.size > 5 * 1024 * 1024) {
    message(card.querySelector(".card-message"), "Use a PNG, JPEG, or WebP image no larger than 5 MiB", "error");
    return;
  }
  const body = new FormData();
  body.append("file", file);
  body.append("runId", state.session.run.id);
  body.append("testId", testId);
  message(card.querySelector(".card-message"), "Uploading screenshot…");
  const response = await fetch(`${config.supabaseUrl}/functions/v1/${config.evidenceFunction || "evidence"}`, {
    method: "POST",
    headers: {
      "x-access-code": state.code,
      apikey: config.supabasePublishableKey,
      Authorization: `Bearer ${config.supabasePublishableKey}`,
    },
    body,
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    message(card.querySelector(".card-message"), payload.error || "Screenshot upload failed", "error");
    return;
  }
  const next = { ...resultFor(testId), evidence_path: payload.path };
  card.querySelector(".evidence-name").textContent = file.name;
  card.querySelector(".view-evidence").classList.remove("hidden");
  await saveResult(next, card);
}

async function viewEvidence(path) {
  if (!path) return;
  const url = new URL(`${config.supabaseUrl}/functions/v1/${config.evidenceFunction || "evidence"}`);
  url.searchParams.set("path", path);
  const response = await fetch(url, { headers: {
    "x-access-code": state.code,
    apikey: config.supabasePublishableKey,
    Authorization: `Bearer ${config.supabasePublishableKey}`,
  } });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) return alert(payload.error || "Could not open screenshot");
  window.open(payload.url, "_blank", "noopener,noreferrer");
}

async function saveProfile() {
  const profile = {
    emulator: $("#profileEmulator").value.trim(),
    device: $("#profileDevice").value.trim(),
    controls: $("#profileControls").value.trim(),
    started: $("#profileStarted").value || null,
  };
  await rpc("save_run_profile", { p_code: state.code, p_run_id: state.session.run.id, p_profile: profile });
  state.session.run.profile = profile;
  message($("#syncMessage"), "Setup details saved", "success");
}

async function openTester(session) {
  state.session = session;
  state.results = new Map((session.results || []).map((row) => [row.test_id, row]));
  $("#testerName").textContent = session.tester.display_name;
  const profile = session.run.profile || {};
  $("#profileEmulator").value = profile.emulator || "";
  $("#profileDevice").value = profile.device || "";
  $("#profileControls").value = profile.controls || "";
  $("#profileStarted").value = profile.started || "";
  show("testerView");
  renderChecklist();
  await retryPending().catch(() => message($("#syncMessage"), "Offline: changes will sync later", "error"));
}

function summaryCard(tester) {
  const card = document.createElement("article");
  card.className = "summary-card";
  const heading = document.createElement("h3");
  heading.textContent = tester.display_name;
  const meta = document.createElement("p");
  meta.textContent = `${tester.completed} of ${state.checklist.count} reviewed`;
  const numbers = document.createElement("div");
  numbers.className = "summary-numbers";
  for (const [label, key] of [["Pass", "passed"], ["Fail", "failed"], ["Skip", "skipped"], ["Left", "not_started"]]) {
    const block = document.createElement("span");
    block.innerHTML = `<strong>${tester[key] || 0}</strong>${label}`;
    numbers.append(block);
  }
  card.append(heading, meta, numbers);
  return card;
}

function renderAdmin(data) {
  state.adminData = data;
  $("#adminSummary").replaceChildren(...(data.testers || []).map(summaryCard));
  const findings = (data.results || []).filter((row) => ["failed", "skipped"].includes(row.status));
  const findingHost = $("#findings");
  findingHost.replaceChildren();
  if (!findings.length) findingHost.textContent = "No failures or skipped tests have been reported.";
  for (const row of findings) {
    const item = state.checklist.items.find((entry) => entry.id === row.test_id);
    const block = document.createElement("article");
    block.className = "finding";
    const title = document.createElement("strong");
    title.textContent = `${row.tester_name} · ${row.test_id} · ${row.status.toUpperCase()}`;
    const copy = document.createElement("p");
    copy.textContent = `${item?.instruction || "Unknown test"} ${row.notes || "No notes supplied."}`;
    block.append(title, copy);
    if (row.evidence_path) {
      const button = document.createElement("button");
      button.className = "quiet";
      button.textContent = "View screenshot";
      button.addEventListener("click", () => viewEvidence(row.evidence_path));
      block.append(button);
    }
    findingHost.append(block);
  }
  const rows = (data.results || []).map((row) => {
    const item = state.checklist.items.find((entry) => entry.id === row.test_id);
    const tr = document.createElement("tr");
    for (const value of [row.tester_name, row.test_id, item?.section || "", row.status, row.notes || "", new Date(row.updated_at).toLocaleString()]) {
      const td = document.createElement("td");
      td.textContent = value;
      tr.append(td);
    }
    return tr;
  });
  $("#resultsTable").replaceChildren(...rows);
  $("#adminUpdated").textContent = `Updated ${new Date().toLocaleString()}`;
}

async function refreshAdmin() {
  const data = await rpc("admin_dashboard", { p_code: state.code });
  if (!data || data.role !== "admin") throw new Error("Administrator access denied");
  renderAdmin(data);
}

function download(name, content, type) {
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([content], { type }));
  link.download = name;
  link.click();
  URL.revokeObjectURL(link.href);
}

function exportJson() {
  download("firered-test-results.json", JSON.stringify(state.adminData, null, 2), "application/json");
}

function exportCsv() {
  const quote = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
  const header = ["tester", "test_id", "section", "status", "notes", "evidence_path", "updated_at"];
  const lines = [header.map(quote).join(",")];
  for (const row of state.adminData?.results || []) {
    const item = state.checklist.items.find((entry) => entry.id === row.test_id);
    lines.push([row.tester_name, row.test_id, item?.section, row.status, row.notes, row.evidence_path, row.updated_at].map(quote).join(","));
  }
  download("firered-test-results.csv", lines.join("\n") + "\n", "text/csv");
}

async function login(code) {
  if (!configured()) throw new Error("This dashboard has not been connected to Supabase yet");
  state.code = code.trim();
  try {
    const session = await rpc("tester_session", { p_code: state.code, p_checklist_version: state.checklist.version });
    if (session?.role === "tester") {
      localStorage.setItem("firered-test-code", state.code);
      await openTester(session);
      return;
    }
  } catch (_) {
    // A tester-code failure may still be a valid administrator code.
  }
  const admin = await rpc("admin_dashboard", { p_code: state.code });
  if (!admin || admin.role !== "admin") throw new Error("Code not recognised");
  localStorage.setItem("firered-test-code", state.code);
  show("adminView");
  renderAdmin(admin);
}

function logout() {
  localStorage.removeItem("firered-test-code");
  state.code = "";
  state.session = null;
  state.results.clear();
  $("#accessCode").value = "";
  show("loginView");
}

$("#loginForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = event.submitter;
  button.disabled = true;
  message($("#loginMessage"), "Checking code…");
  try {
    await login($("#accessCode").value);
    message($("#loginMessage"), "");
  } catch (error) {
    message($("#loginMessage"), error.message, "error");
  } finally {
    button.disabled = false;
  }
});
$("#logoutButton").addEventListener("click", logout);
$("#statusFilter").addEventListener("change", applyFilters);
$("#searchInput").addEventListener("input", applyFilters);
$("#retrySync").addEventListener("click", () => retryPending().catch((error) => message($("#syncMessage"), error.message, "error")));
$("#saveProfile").addEventListener("click", () => saveProfile().catch((error) => message($("#syncMessage"), error.message, "error")));
$("#refreshAdmin").addEventListener("click", () => refreshAdmin().catch((error) => message($("#adminUpdated"), error.message, "error")));
$("#exportJson").addEventListener("click", exportJson);
$("#exportCsv").addEventListener("click", exportCsv);

(async () => {
  try {
    await loadChecklist();
    if (state.code && configured()) await login(state.code);
    else show("loginView");
    if (!configured()) message($("#loginMessage"), "Dashboard setup is incomplete. Add the Supabase project settings to deploy it.", "error");
  } catch (error) {
    show("loginView");
    message($("#loginMessage"), error.message, "error");
  }
})();
