const BASE = "http://localhost:8000";

async function apiFetch(path, options = {}) {
  const init = {
    method: options.method || "GET",
    headers: { "Content-Type": "application/json" },
  };
  if (options.body !== undefined) {
    init.body = JSON.stringify(options.body);
  }
  const res = await fetch(BASE + path, init);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

export const api = {
  health:      () => apiFetch("/health"),
  getSolver:   () => apiFetch("/config/solver"),
  setSolver:   (name) => apiFetch("/config/solver", { method: "PUT", body: { solver: name } }),
  getParams:   () => apiFetch("/params"),
  updateParams: (body) => apiFetch("/params", { method: "PUT", body }),
  resetParams: () => apiFetch("/params/reset", { method: "POST" }),
  solveLgp:    () => apiFetch("/solve/lgp", { method: "POST" }),
  solveEr:     (steps) => apiFetch("/solve/er", { method: "POST", body: { steps } }),
};
