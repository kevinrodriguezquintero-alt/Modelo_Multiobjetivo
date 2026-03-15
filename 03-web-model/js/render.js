// ── Helpers ────────────────────────────────────────────────────────────────

function fmt(n) {
  if (n === null || n === undefined) return "—";
  return typeof n === "number" ? n.toLocaleString("es-CO", { maximumFractionDigits: 4 }) : String(n);
}

function statusBadge(status) {
  const ok = status === "optimal";
  return `<span class="badge ${ok ? "badge-ok" : "badge-err"}">${status}</span>`;
}

function th(...cols) {
  return `<tr>${cols.map(c => `<th>${c}</th>`).join("")}</tr>`;
}

function td(...cols) {
  return `<tr>${cols.map(c => `<td>${c}</td>`).join("")}</tr>`;
}

// ── Inner tabs (Resultado / Logs) ───────────────────────────────────────────

function renderInnerTabs(ns, tabs) {
  const btnHtml = tabs.map((t, i) => `
    <button class="inner-tab-btn ${i === 0 ? "inner-tab-active" : ""}"
            data-inner-ns="${ns}" data-inner-tab="${t.id}">
      ${t.label}
    </button>`).join("");

  const paneHtml = tabs.map((t, i) => `
    <div class="inner-pane ${i === 0 ? "" : "hidden"}"
         data-inner-ns="${ns}" data-inner-pane="${t.id}">
      ${t.content}
    </div>`).join("");

  return `
    <div class="inner-tabs-bar">${btnHtml}</div>
    <div class="inner-panes">${paneHtml}</div>`;
}

function renderTerminal(text) {
  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
  return `
    <div class="terminal-wrap">
      <div class="terminal-header">
        <span class="terminal-title">Solver output</span>
        <button class="copy-btn" onclick="
          navigator.clipboard.writeText(this.closest('.terminal-wrap').querySelector('pre').textContent);
          this.textContent='Copiado';
          setTimeout(()=>this.textContent='Copiar',1800);
        ">Copiar</button>
      </div>
      <pre class="terminal-body">${escaped || "(sin output)"}</pre>
    </div>`;
}

// ── LGP ────────────────────────────────────────────────────────────────────

export function renderLgpResult(data) {
  if (!data) return `<p class="text-red-500">Sin datos.</p>`;

  const stepsHtml = (data.steps || []).map(s => {
    const objs = s.objectives || {};
    return `
      <div class="step-card">
        <div class="step-header">
          <span class="step-num">Paso ${s.step}</span>
          <span class="step-priority">${s.priority}</span>
          ${statusBadge(s.status)}
        </div>
        <table class="data-table mt-2">
          <thead>${th("Objetivo", "Valor")}</thead>
          <tbody>
            ${td("Costo", fmt(objs.cost))}
            ${td("Emisiones", fmt(objs.emissions))}
            ${td("Empleo", fmt(objs.employment))}
          </tbody>
        </table>
      </div>`;
  }).join("");

  const vars = data.variables;
  let varsHtml = "";
  if (vars) {
    varsHtml = `
      <h3 class="section-subtitle">Variables de decisión</h3>
      <div class="vars-grid">
        ${renderVarTable("X — Flujo productor→intermediario", ["i", "j", "value"], vars.X)}
        ${renderVarTable("Y — Flujo intermediario→retailer", ["j", "k", "value"], vars.Y)}
        ${renderVarTable("Z — Viajes productor→intermediario", ["i", "j", "value"], vars.Z)}
        ${renderVarTable("ZZ — Viajes intermediario→retailer", ["j", "k", "value"], vars.ZZ)}
        ${renderVarTable("W — Hectáreas por productor", ["i", "value"], vars.W)}
        ${renderVarTable("S — Personal intermediario", ["j", "value"], vars.S)}
        ${renderVarTable("SS — Personal retailer", ["k", "value"], vars.SS)}
        ${renderVarTable("B — Variantes activas", ["u", "value"], vars.B)}
      </div>`;
  }

  // Logs: one entry per step (log field added by backend)
  const combinedLog = (data.steps || [])
    .map(s => `=== Paso ${s.step} — ${s.priority} ===\n${s.log || "(sin log)"}`)
    .join("\n");

  return `
    <div class="result-status mb-4">
      <strong>Estado final:</strong> ${statusBadge(data.status)}
      &nbsp; <strong>Solver:</strong> <code>${data.solver}</code>
    </div>
    ${renderInnerTabs("lgp", [
      { id: "resultado", label: "Resultado", content: `
        <h3 class="section-subtitle">Pasos LGP</h3>
        <div class="steps-grid">${stepsHtml}</div>
        ${varsHtml}` },
      { id: "logs", label: "Logs", content: renderTerminal(combinedLog) },
    ])}`;
}

function renderVarTable(title, cols, rows) {
  if (!rows || rows.length === 0) return "";
  const header = th(...cols.map(c => c.toUpperCase()));
  const body = rows.map(r => td(...cols.map(c => fmt(r[c])))).join("");
  return `
    <div class="var-block">
      <h4 class="var-title">${title}</h4>
      <table class="data-table">
        <thead>${header}</thead>
        <tbody>${body}</tbody>
      </table>
    </div>`;
}

// ── ER ─────────────────────────────────────────────────────────────────────

export function renderErResult(data) {
  if (!data) return `<p class="text-red-500">Sin datos.</p>`;

  // Payoff table
  const pt = data.payoff_table || {};
  const payoffHtml = `
    <h3 class="section-subtitle">Tabla Payoff</h3>
    <table class="data-table">
      <thead>${th("Escenario", "Costo", "Emisiones", "Empleo")}</thead>
      <tbody>
        ${td("Min Costo",      fmt(pt.min_cost?.cost),      fmt(pt.min_cost?.emissions),      fmt(pt.min_cost?.employment))}
        ${td("Min Emisiones",  fmt(pt.min_emissions?.cost), fmt(pt.min_emissions?.emissions), fmt(pt.min_emissions?.employment))}
        ${td("Max Social",     fmt(pt.max_social?.cost),    fmt(pt.max_social?.emissions),    fmt(pt.max_social?.employment))}
      </tbody>
    </table>`;

  // Pareto frontier table
  const pf = data.pareto_frontier || [];
  const paretoRows = pf.map(p => {
    const o = p.objectives || {};
    return td(p.iteration, fmt(p.epsilon), statusBadge(p.status), fmt(o.cost), fmt(o.emissions), fmt(o.employment));
  }).join("");
  const paretoHtml = `
    <h3 class="section-subtitle mt-6">Frontera Pareto</h3>
    <table class="data-table">
      <thead>${th("Iter", "ε (Emisiones)", "Estado", "Costo", "Emisiones", "Empleo")}</thead>
      <tbody>${paretoRows}</tbody>
    </table>`;

  // Last iteration variables
  const vars = data.last_iteration_variables;
  const varsHtml = vars ? `
    <h3 class="section-subtitle mt-6">Variables — última iteración óptima</h3>
    <div class="vars-grid">
      ${renderVarTable("X — Flujo productor→intermediario", ["i", "j", "value"], vars.X)}
      ${renderVarTable("Y — Flujo intermediario→retailer", ["j", "k", "value"], vars.Y)}
      ${renderVarTable("Z — Viajes productor→intermediario", ["i", "j", "value"], vars.Z)}
      ${renderVarTable("ZZ — Viajes intermediario→retailer", ["j", "k", "value"], vars.ZZ)}
      ${renderVarTable("W — Hectáreas por productor", ["i", "value"], vars.W)}
      ${renderVarTable("S — Personal intermediario", ["j", "value"], vars.S)}
      ${renderVarTable("SS — Personal retailer", ["k", "value"], vars.SS)}
      ${renderVarTable("B — Variantes activas", ["u", "value"], vars.B)}
    </div>` : "";

  return `
    <div class="result-status mb-4">
      <strong>Solver:</strong> <code>${data.solver}</code>
      &nbsp; <strong>Steps:</strong> ${data.steps}
    </div>
    ${renderInnerTabs("er", [
      { id: "resultado", label: "Resultado", content: `
        ${payoffHtml}
        ${paretoHtml}
        <h3 class="section-subtitle mt-6">Dispersión Costo vs Emisiones</h3>
        <div class="scatter-wrap">
          <canvas id="pareto-chart"></canvas>
        </div>
        ${varsHtml}` },
      { id: "logs", label: "Logs", content: renderTerminal(data.log || "") },
    ])}`;
}

// ── Params (editable) ───────────────────────────────────────────────────────

const PARAM_DESCRIPTIONS = {
  PRODUCERS:         "Conjunto de productores (I)",
  INTERMEDIARIES:    "Conjunto de intermediarios (J)",
  RETAILERS:         "Conjunto de detallistas (K)",
  PRODUCER_VARIANTS: "Variantes de productor (U)",
  RB:  "Rendimiento máximo total (Kg/Ha·semana)",
  RA:  "Rendimiento por variante de productor u (Kg/Ha·semana)",
  RC:  "Rendimiento máximo del cultivo base por productor i (Kg/Ha·semana)",
  RD:  "Rendimiento mínimo del cultivo base por productor i (Kg/Ha·semana)",
  CA:  "Capacidad productiva por persona en intermediario j (Kg/persona)",
  CB:  "Capacidad productiva por persona en detallista k (Kg/persona)",
  CP:  "Costo de producción en productor i ($/Kg)",
  CI:  "Costo de procesamiento en intermediario j ($/Kg)",
  CT:  "Costo de transporte productor i → intermediario j ($/Kg)",
  CTT: "Costo de transporte intermediario j → detallista k ($/Kg)",
  CD:  "Costo de mano de obra en detallista k ($/semana)",
  CDA: "Costo por daño en ruta productor i → intermediario j ($/Kg)",
  CDF: "Costo por daño en ruta intermediario j → detallista k ($/Kg)",
  P:   "Porcentaje de daño productor i → intermediario j (%)",
  PP:  "Porcentaje de daño intermediario j → detallista k (%)",
  CN:  "Capacidad de producción en productor i (Kg/día)",
  CH:  "Capacidad de despacho en productor i (Kg/día)",
  CHI: "Capacidad de despacho en intermediario j (Kg/día)",
  CR:  "Capacidad de recepción en detallista k (Kg/día)",
  DI:  "Demanda mínima en intermediario j (Kg/día)",
  DD:  "Demanda mínima en detallista k (Kg/día)",
  CV:  "Capacidad del vehículo en intermediario j (Kg/viaje)",
  CMO: "Costo de mano de obra en intermediario j ($/semana)",
  H:   "Número de hectáreas por variante de productor u (Ha·semana)",
  DPI: "Distancia/impacto ambiental ruta productor i → intermediario j (km)",
  DID: "Distancia/impacto ambiental ruta intermediario j → detallista k (km)",
  IT:  "Factor de impacto de transporte por intermediario j",
};

export function renderParams(data) {
  if (!data) return `<p class="text-red-500">Sin datos.</p>`;

  const rows = Object.entries(data).map(([key, val]) => {
    let kind, inputHtml;

    if (typeof val === "number") {
      // scalar
      kind = "scalar";
      inputHtml = `<input type="number" step="any" class="param-input"
        data-param="${key}" data-kind="scalar" value="${val}">`;

    } else if (Array.isArray(val)) {
      if (val.length === 0 || typeof val[0] !== "object") {
        // list of primitives
        kind = "list";
        inputHtml = `<input type="text" class="param-input param-input-list"
          data-param="${key}" data-kind="list" value="${val.join(", ")}">`;
      } else {
        // dict2: [{k1, k2, value}, ...]
        kind = "dict2";
        const keys = Object.keys(val[0]).filter(k => k !== "value");
        const k1name = keys[0], k2name = keys[1];
        const bodyRows = val.map(entry => `
          <tr>
            <td class="idx-cell">${entry[k1name]}</td>
            <td class="idx-cell">${entry[k2name]}</td>
            <td><input type="number" step="any" class="param-input"
                  data-param="${key}" data-kind="dict2"
                  data-k1name="${k1name}" data-k1val="${entry[k1name]}"
                  data-k2name="${k2name}" data-k2val="${entry[k2name]}"
                  value="${entry.value}"></td>
          </tr>`).join("");
        inputHtml = `
          <div class="dict2-wrap">
            <table class="data-table dict2-table">
              <thead>${th(k1name.toUpperCase(), k2name.toUpperCase(), "Valor")}</thead>
              <tbody>${bodyRows}</tbody>
            </table>
          </div>`;
      }

    } else if (typeof val === "object" && val !== null) {
      // dict1: {"1": v, "2": v, ...}
      kind = "dict1";
      const pairs = Object.entries(val).map(([k, v]) => `
        <span class="dict1-key">${k}</span>
        <input type="number" step="any" class="param-input"
               data-param="${key}" data-kind="dict1" data-key="${k}"
               value="${v}">`).join("");
      inputHtml = `<div class="dict1-grid">${pairs}</div>`;

    } else {
      kind = typeof val;
      inputHtml = String(val ?? "—");
    }

    const desc = PARAM_DESCRIPTIONS[key] ?? "";
    return `
      <tr>
        <td><strong>${key}</strong></td>
        <td class="param-desc">${desc}</td>
        <td><span class="type-tag">${kind}</span></td>
        <td>${inputHtml}</td>
      </tr>`;
  }).join("");

  return `
    <table class="data-table params-table">
      <thead>${th("Parámetro", "Descripción", "Tipo", "Valor / Editar")}</thead>
      <tbody>${rows}</tbody>
    </table>`;
}

// ── Solver Config ──────────────────────────────────────────────────────────

export function renderSolverConfig(data, badgeEl, selectEl) {
  if (!data) return;
  if (badgeEl) {
    badgeEl.textContent = data.active || data.solver || "—";
    badgeEl.className = "solver-badge";
  }
  if (selectEl && data.available) {
    const current = selectEl.value || data.active;
    selectEl.innerHTML = data.available
      .map(s => `<option value="${s}" ${s === current ? "selected" : ""}>${s}</option>`)
      .join("");
  }
}
