import { api } from "./api.js";
import { renderLgpResult, renderErResult, renderParams, renderSolverConfig } from "./render.js";

// ── Tab switching ──────────────────────────────────────────────────────────

function initTabs() {
  const tabs = document.querySelectorAll("[data-tab]");
  const sections = document.querySelectorAll("section[id^='tab-']");

  function activateTab(name) {
    tabs.forEach(t => t.classList.toggle("tab-active", t.dataset.tab === name));
    sections.forEach(s => s.classList.toggle("hidden", s.id !== `tab-${name}`));
    const url = new URL(window.location);
    url.searchParams.set("tab", name);
    history.replaceState(null, "", url);
  }

  tabs.forEach(t => t.addEventListener("click", () => activateTab(t.dataset.tab)));

  const initial = new URL(window.location).searchParams.get("tab") || "config";
  activateTab(initial);
}

// ── Spinner helpers ────────────────────────────────────────────────────────

function showSpinner(el) {
  el.innerHTML = `<div class="spinner" role="status" aria-label="Cargando…"></div>`;
}

function showError(el, msg) {
  el.innerHTML = `<div class="error-box"><strong>Error:</strong> ${msg}</div>`;
}

// ── Config ─────────────────────────────────────────────────────────────────

function initConfig() {
  const badge  = document.getElementById("solver-badge");
  const select = document.getElementById("solver-select");
  const btn    = document.getElementById("solver-btn");
  const msg    = document.getElementById("solver-msg");

  async function loadSolver() {
    try {
      const data = await api.getSolver();
      renderSolverConfig(data, badge, select);
    } catch (e) {
      if (badge) badge.textContent = "error";
    }
  }

  btn.addEventListener("click", async () => {
    msg.textContent = "";
    try {
      const data = await api.setSolver(select.value);
      renderSolverConfig(data, badge, select);
      msg.textContent = `Solver cambiado a "${select.value}".`;
      msg.className = "feedback-ok";
    } catch (e) {
      msg.textContent = e.message;
      msg.className = "feedback-err";
    }
  });

  loadSolver();
}

// ── Params ─────────────────────────────────────────────────────────────────

function collectParamsPatch(container) {
  const patch = {};
  container.querySelectorAll(".param-input").forEach(input => {
    const { param, kind } = input.dataset;
    const raw = input.value;

    if (kind === "scalar") {
      patch[param] = parseFloat(raw);
    } else if (kind === "list") {
      patch[param] = raw.split(",").map(x => parseInt(x.trim(), 10)).filter(x => !isNaN(x));
    } else if (kind === "dict1") {
      if (!patch[param]) patch[param] = {};
      patch[param][input.dataset.key] = parseFloat(raw);
    } else if (kind === "dict2") {
      if (!patch[param]) patch[param] = [];
      const { k1name, k1val, k2name, k2val } = input.dataset;
      patch[param].push({
        [k1name]: parseInt(k1val, 10),
        [k2name]: parseInt(k2val, 10),
        value: parseFloat(raw),
      });
    }
  });
  return patch;
}

function initParams() {
  const container = document.getElementById("params-container");
  const saveBtn   = document.getElementById("params-save-btn");
  const resetBtn  = document.getElementById("params-reset-btn");
  const msg       = document.getElementById("params-msg");

  async function loadParams() {
    showSpinner(container);
    try {
      const data = await api.getParams();
      container.innerHTML = renderParams(data);
    } catch (e) {
      showError(container, e.message);
    }
  }

  saveBtn.addEventListener("click", async () => {
    msg.textContent = "";
    try {
      const patch = collectParamsPatch(container);
      await api.updateParams(patch);
      msg.textContent = "Parámetros guardados.";
      msg.className = "feedback-ok";
    } catch (e) {
      msg.textContent = e.message;
      msg.className = "feedback-err";
    }
  });

  resetBtn.addEventListener("click", async () => {
    msg.textContent = "";
    try {
      await api.resetParams();
      msg.textContent = "Parámetros restaurados.";
      msg.className = "feedback-ok";
      loadParams();
    } catch (e) {
      msg.textContent = e.message;
      msg.className = "feedback-err";
    }
  });

  loadParams();
}

// ── LGP ────────────────────────────────────────────────────────────────────

function initLgp() {
  const btn       = document.getElementById("lgp-btn");
  const container = document.getElementById("lgp-result");

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    showSpinner(container);
    try {
      const data = await api.solveLgp();
      container.innerHTML = renderLgpResult(data);
    } catch (e) {
      showError(container, e.message);
    } finally {
      btn.disabled = false;
    }
  });
}

// ── ER ─────────────────────────────────────────────────────────────────────

function drawErChart(pareto) {
  const canvas = document.getElementById("pareto-chart");
  if (!canvas) return;

  const points = (pareto || [])
    .filter(p => p.status === "optimal" && p.objectives)
    .sort((a, b) => a.objectives.emissions - b.objectives.emissions)
    .map(p => ({ x: p.objectives.emissions, y: p.objectives.cost }));

  if (points.length === 0) {
    canvas.parentElement.innerHTML =
      `<p class="text-gray-400 italic">Sin puntos óptimos para graficar.</p>`;
    return;
  }

  new Chart(canvas, {
    type: "scatter",
    data: {
      datasets: [{
        label: "Frontera Pareto",
        data: points,
        backgroundColor: "rgba(99, 102, 241, 0.75)",
        borderColor: "#6366f1",
        pointRadius: 6,
        pointHoverRadius: 9,
        showLine: true,
        borderWidth: 1.5,
        borderDash: [5, 4],
        tension: 0,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx =>
              `Emisiones: ${ctx.parsed.x.toFixed(4)}   Costo: ${ctx.parsed.y.toFixed(4)}`,
          },
        },
      },
      scales: {
        x: { title: { display: true, text: "Emisiones" } },
        y: { title: { display: true, text: "Costo" } },
      },
    },
  });
}

function initEr() {
  const btn        = document.getElementById("er-btn");
  const stepsInput = document.getElementById("er-steps");
  const container  = document.getElementById("er-result");

  btn.addEventListener("click", async () => {
    const steps = parseInt(stepsInput.value, 10) || 5;
    btn.disabled = true;
    showSpinner(container);
    try {
      const data = await api.solveEr(steps);
      container.innerHTML = renderErResult(data);
      drawErChart(data.pareto_frontier);
    } catch (e) {
      showError(container, e.message);
    } finally {
      btn.disabled = false;
    }
  });
}

// ── Inner tabs (delegated, works after innerHTML injection) ────────────────

function initInnerTabs() {
  document.addEventListener("click", e => {
    const btn = e.target.closest(".inner-tab-btn");
    if (!btn) return;
    const ns   = btn.dataset.innerNs;
    const tabId = btn.dataset.innerTab;
    const scope = btn.closest(".inner-panes")?.parentElement
               ?? document;

    scope.querySelectorAll(`.inner-tab-btn[data-inner-ns="${ns}"]`)
      .forEach(b => b.classList.toggle("inner-tab-active", b === btn));
    scope.querySelectorAll(`.inner-pane[data-inner-ns="${ns}"]`)
      .forEach(p => p.classList.toggle("hidden", p.dataset.innerPane !== tabId));
  });
}

// ── Boot ───────────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initInnerTabs();
  initConfig();
  initParams();
  initLgp();
  initEr();
});
