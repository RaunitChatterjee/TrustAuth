/* ==========================================================================
   TrustAuth — main.js
   Minimal vanilla JS: icon rendering, UI interactions, and a client-side
   keystroke-dynamics capture used to demonstrate continuous behavioral
   authentication. In production, captured events should be POSTed to a
   Flask endpoint (e.g. /api/behavior-event) where a trained model scores
   the session. Here, scoring is simulated locally so the UI is interactive
   without requiring the ML backend to be wired up yet.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initIcons();
  initSidebarToggle();
  initPasswordToggles();
  initKeystrokeCapture("password");   // login / register
  initKeystrokeCapture("note");       // transfer note field
  initKeystrokeCapture("amount");     // transfer amount field
});

/* ---------------------------------------------------------------------- */
function initIcons() {
  if (window.lucide) {
    lucide.createIcons();
  } else {
    // lucide script may still be loading; retry once it's ready
    window.addEventListener("load", () => window.lucide && lucide.createIcons());
  }
}

/* ---------------------------------------------------------------------- */
function initSidebarToggle() {
  const btn = document.getElementById("sidebarToggle");
  const sidebar = document.getElementById("sidebar");
  if (!btn || !sidebar) return;

  btn.addEventListener("click", () => sidebar.classList.toggle("is-open"));

  document.addEventListener("click", (e) => {
    if (
      sidebar.classList.contains("is-open") &&
      !sidebar.contains(e.target) &&
      e.target !== btn &&
      !btn.contains(e.target)
    ) {
      sidebar.classList.remove("is-open");
    }
  });
}

/* ---------------------------------------------------------------------- */
function initPasswordToggles() {
  document.querySelectorAll(".toggle-visibility").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      const input = document.getElementById(targetId);
      if (!input) return;
      const isHidden = input.type === "password";
      input.type = isHidden ? "text" : "password";
      btn.innerHTML = isHidden
        ? '<i data-lucide="eye-off"></i>'
        : '<i data-lucide="eye"></i>';
      if (window.lucide) lucide.createIcons();
    });
  });
}

/* ==========================================================================
   Keystroke Dynamics Capture
   Records dwell time (keydown -> keyup on the same key) and flight time
   (keyup of one key -> keydown of the next) for a given input field.
   This is the raw signal a real TrustAuth backend would use to build a
   per-user typing profile and to score live sessions for anomalies.
   ========================================================================== */
function initKeystrokeCapture(fieldId) {
  const field = document.getElementById(fieldId);
  if (!field) return;

  const keyDownTimes = {};
  let lastKeyUpTime = null;
  const events = []; // { key, dwell, flight, timestamp }

  field.addEventListener("keydown", (e) => {
    if (!(e.key in keyDownTimes)) {
      keyDownTimes[e.key] = performance.now();
    }
  });

  field.addEventListener("keyup", (e) => {
    const downTime = keyDownTimes[e.key];
    const upTime = performance.now();
    if (downTime == null) return;

    const dwell = upTime - downTime;
    const flight = lastKeyUpTime != null ? downTime - lastKeyUpTime : null;

    events.push({
      key: e.key.length === 1 ? "char" : e.key, // avoid logging literal characters
      dwell: Math.round(dwell),
      flight: flight != null ? Math.round(flight) : null,
      timestamp: Date.now(),
    });

    lastKeyUpTime = upTime;
    delete keyDownTimes[e.key];

    onKeystrokeEvent(fieldId, events);
  });
}

/* Called on every captured keystroke. Updates the live trust widgets on the
   page (if present) with a simulated score derived from typing variance.
   Swap simulateScoreFromEvents() for a real fetch() to your Flask/ML
   endpoint once the backend is ready. */
function onKeystrokeEvent(fieldId, events) {
  updateKeystrokeMeta(events);

  // Example of how this would talk to a real backend:
  //
  // fetch("/api/behavior-event", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ field: fieldId, events: events.slice(-1) }),
  // })
  //   .then((res) => res.json())
  //   .then((data) => applyTrustScore(data.score, data.risk));

  const { score, risk } = simulateScoreFromEvents(events);
  applyTrustScore(score, risk);
}

/* Simple local heuristic used only for the demo: high variance in dwell
   time relative to the running average is treated as more "anomalous". */
function simulateScoreFromEvents(events) {
  if (events.length < 4) return { score: 98, risk: "low" };

  const recent = events.slice(-12).map((e) => e.dwell);
  const mean = recent.reduce((a, b) => a + b, 0) / recent.length;
  const variance =
    recent.reduce((a, b) => a + (b - mean) ** 2, 0) / recent.length;
  const stdDev = Math.sqrt(variance);

  // Map coefficient of variation to a 0-100 score. This is illustrative
  // only, not a real trained model.
  const coeffVar = mean > 0 ? stdDev / mean : 0;
  let score = Math.round(100 - coeffVar * 120);
  score = Math.max(35, Math.min(99, score));

  const risk = score >= 80 ? "low" : score >= 55 ? "medium" : "high";
  return { score, risk };
}

function updateKeystrokeMeta(events) {
  const countEl = document.getElementById("keystrokeCount");
  const dwellEl = document.getElementById("dwellAvg");
  if (countEl) countEl.textContent = events.length;
  if (dwellEl && events.length) {
    const avg =
      events.reduce((a, e) => a + e.dwell, 0) / events.length;
    dwellEl.textContent = `${Math.round(avg)} ms`;
  }
}

/* Applies a trust score to every trust widget currently on the page. */
function applyTrustScore(score, risk) {
  document.querySelectorAll("[data-risk]").forEach((el) => {
    el.setAttribute("data-risk", risk);
  });

  const valueEls = document.querySelectorAll(
    ".trust-widget__value, .trust-card__score"
  );
  valueEls.forEach((el) => {
    // Preserve a trailing "/100" span inside .trust-card__score if present
    const suffix = el.querySelector("span");
    el.textContent = score;
    if (suffix) el.appendChild(suffix);
  });

  const badge = document.getElementById("transferRiskBadge");
  if (badge) {
    badge.textContent =
      risk === "low" ? "Low Risk" : risk === "medium" ? "Elevated Risk" : "High Risk";
    badge.setAttribute("data-risk", risk);
  }

  const statusLabel = document.getElementById("statusLabel");
  if (statusLabel) {
    statusLabel.textContent =
      risk === "low" ? "Monitoring" : risk === "medium" ? "Reviewing" : "Step-up required";
  }

  const scoreValueEl = document.getElementById("transferScoreValue");
  if (scoreValueEl) {
    const suffix = scoreValueEl.querySelector("span");
    scoreValueEl.textContent = score;
    if (suffix) scoreValueEl.appendChild(suffix);
  }
}
