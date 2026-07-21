const byId = (id) => document.getElementById(id);

async function request(url, options) {
  const response = await fetch(url, options);
  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json") ? await response.json() : await response.text();
  if (!response.ok) throw new Error(typeof body === "string" ? body : JSON.stringify(body));
  return body;
}
 
function show(id, value) {
  byId(id).textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

async function loadStatus() {
  const statuses = await request("/api/status");
  byId("status-grid").innerHTML = Object.entries(statuses).map(([name, value]) =>
    `<article><strong>${name}</strong><span>${value.status || "unknown"}</span></article>`
  ).join("");
}

async function loadComments() {
  const comments = await request("/api/comments");
  // INTENTIONAL STORED XSS: untrusted API values are inserted into innerHTML.
  byId("comments").innerHTML = comments.map((comment) =>
    `<article><strong>${comment.author}</strong><p>${comment.text}</p></article>`
  ).join("");
}

byId("refresh-status").addEventListener("click", () => loadStatus().catch((e) => show("status-grid", e.message)));

byId("search-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try { show("search-output", await request(`/api/search?q=${encodeURIComponent(byId("search-query").value)}`)); }
  catch (e) { show("search-output", e.message); }
});

byId("diagnostic-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try { show("diagnostic-output", await request(`/api/diagnostics?host=${encodeURIComponent(byId("diagnostic-host").value)}`)); }
  catch (e) { show("diagnostic-output", e.message); }
});

byId("file-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try { show("file-output", await request(`/api/files?name=${encodeURIComponent(byId("file-name").value)}`)); }
  catch (e) { show("file-output", e.message); }
});

byId("report-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try { show("report-output", await request(`/api/report?name=${encodeURIComponent(byId("report-name").value)}`)); }
  catch (e) { show("report-output", e.message); }
});

byId("java-user").addEventListener("click", async () => show("access-output", await request("/api/java/users?id=2")));
byId("csharp-account").addEventListener("click", async () => show("access-output", await request("/api/csharp/accounts/2")));
byId("admin-config").addEventListener("click", async () => show("access-output", await request("/api/admin/config")));

byId("comment-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  await request("/api/comments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ author: byId("comment-author").value, text: byId("comment-text").value })
  });
  await loadComments();
});

loadStatus().catch(console.error);
loadComments().catch(console.error);
