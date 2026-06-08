const statusOrder = ["healthy", "warning", "degraded", "critical", "unknown"];

function normalizeStatus(status) {
  return statusOrder.includes(status) ? status : "unknown";
}

function updateCard(check) {
  const card = document.querySelector(`[data-check="${check.name}"]`);
  if (!card) {
    return;
  }

  const status = normalizeStatus(check.status);
  const displayStatus = check.ignored ? "Not configured" : status;
  card.classList.remove(...statusOrder);
  card.classList.add(status);
  card.querySelector("h3").textContent = displayStatus;
  card.querySelector(".message").textContent = check.message;
  updateDetails(card, check);
}

function setDetail(card, key, value) {
  const detail = card.querySelector(`[data-detail="${key}"]`);
  if (!detail) {
    return;
  }
  detail.textContent = value ?? "--";
}

function updateDetails(card, check) {
  const details = check.details || {};

  if (check.name === "traffic") {
    setDetail(card, "estimated_used_gb", formatGb(details.estimated_used_gb));
    setDetail(card, "monthly_limit_gb", formatGb(details.monthly_limit_gb));
    setDetail(card, "usage_percent", formatPercent(details.usage_percent));
  }

  if (check.name === "domain_dns") {
    const resolved = details.resolved_ips || {};
    const resolvedCount = Object.values(resolved).reduce((count, ips) => count + (Array.isArray(ips) ? ips.length : 0), 0);
    const hasExpected = Array.isArray(details.expected_ips) && details.expected_ips.length > 0;
    const mismatchCount = Array.isArray(details.mismatches) ? details.mismatches.length : 0;
    let expectedMatch = "not configured";
    if (hasExpected && !check.ignored) {
      expectedMatch = mismatchCount === 0 ? "yes" : "no";
    }
    setDetail(card, "resolved_ip_count", check.ignored ? "not configured" : resolvedCount);
    setDetail(card, "expected_match", expectedMatch);
  }

  if (check.name === "tls_certificate") {
    const targets = Array.isArray(details.targets) ? details.targets : [];
    const firstTarget = targets[0] || {};
    setDetail(card, "days_remaining", check.ignored ? "not configured" : firstTarget.days_remaining);
    setDetail(card, "not_after", check.ignored ? "not configured" : formatDate(firstTarget.not_after));
  }
}

function formatGb(value) {
  if (typeof value !== "number") {
    return "--";
  }
  return `${value.toFixed(2)} GB`;
}

function formatPercent(value) {
  if (typeof value !== "number") {
    return "--";
  }
  return `${value.toFixed(1)}%`;
}

function formatDate(value) {
  if (!value) {
    return "--";
  }
  return new Date(value).toLocaleDateString();
}

function renderHealth(data) {
  const overallStatus = normalizeStatus(data.overall_status);
  const badge = document.getElementById("overall-badge");
  badge.classList.remove(...statusOrder);
  badge.classList.add(overallStatus);
  badge.textContent = overallStatus;

  document.getElementById("overall-status").textContent = `Overall Status: ${overallStatus}`;
  document.getElementById("readable-summary").textContent = data.readable_summary;
  document.getElementById("last-checked").textContent = `Last Checked: ${new Date(data.checked_at).toLocaleString()}`;

  data.checks.forEach(updateCard);

  const riskList = document.getElementById("risk-summary");
  riskList.replaceChildren();
  data.risk_summary.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    riskList.appendChild(li);
  });
}

function renderAlertStatus(data) {
  const alerts = data.alerts || {};
  const telegram = data.telegram || {};
  const email = data.email || {};
  const state = data.state || {};
  document.getElementById("alerts-enabled").textContent = alerts.enabled ? "Enabled" : "Disabled";
  document.getElementById("alerts-message").textContent = alerts.enabled
    ? "Alerts can send notifications when health reaches the configured severity."
    : "Alerts are disabled; no notifications will be sent.";
  document.getElementById("alerts-min-severity").textContent = alerts.min_severity || "--";
  document.getElementById("alerts-cooldown").textContent = `${alerts.cooldown_seconds ?? "--"}s`;
  document.getElementById("alerts-telegram").textContent = telegram.enabled ? "Enabled" : "Disabled";
  document.getElementById("alerts-email").textContent = email.enabled ? "Enabled" : "Disabled";
  document.getElementById("alerts-active").textContent = state.active_alert_count ?? "--";
  document.getElementById("alerts-last-sent").textContent = state.last_sent_at
    ? new Date(state.last_sent_at).toLocaleString()
    : "--";
}

async function refreshAlertStatus() {
  try {
    const response = await fetch("/api/alerts/status", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderAlertStatus(await response.json());
  } catch (error) {
    document.getElementById("alerts-message").textContent = `Alert status unavailable: ${error.message}`;
  }
}

function renderDiagnostics(data) {
  document.getElementById("diagnostics-summary").textContent = data.summary || "No diagnostics summary available.";
  const item = Array.isArray(data.items) ? data.items[0] : null;
  if (!item) {
    return;
  }
  document.querySelector("#top-diagnosis h3").textContent = `${item.title} (${item.severity})`;
  document.getElementById("diagnosis-impact").textContent = `Impact: ${item.impact}`;
  document.getElementById("diagnosis-first-check").textContent = `Suggested first check: ${item.suggested_first_check}`;
  document.getElementById("diagnosis-related").textContent = `Related modules: ${(item.related_modules || []).join(", ") || "--"}`;
  document.getElementById("diagnosis-confidence").textContent = `Confidence: ${item.confidence}`;
  document.getElementById("diagnosis-commands").textContent = (item.read_only_commands || []).join("\n") || "No command needed.";
}

async function refreshDiagnostics() {
  try {
    const response = await fetch("/api/diagnostics", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderDiagnostics(await response.json());
  } catch (error) {
    document.getElementById("diagnostics-summary").textContent = `Diagnostics unavailable: ${error.message}`;
  }
}

async function sendTestAlert() {
  const output = document.getElementById("test-alert-result");
  output.textContent = "Sending test alert...";
  try {
    const response = await fetch("/api/alerts/test", { method: "POST" });
    const data = await response.json();
    output.textContent = data.sent ? "Test alert sent." : data.message || "Test alert skipped.";
    await refreshAlertStatus();
  } catch (error) {
    output.textContent = `Test alert failed: ${error.message}`;
  }
}

async function refreshHealth() {
  try {
    const response = await fetch("/api/health", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderHealth(await response.json());
  } catch (error) {
    renderHealth({
      overall_status: "unknown",
      readable_summary: "Dashboard could not load health data from the local API.",
      checked_at: new Date().toISOString(),
      risk_summary: [`api: ${error.message}`],
      checks: [],
    });
  }
}

refreshHealth();
refreshAlertStatus();
refreshDiagnostics();
document.getElementById("test-alert-button").addEventListener("click", sendTestAlert);
window.setInterval(refreshHealth, 30000);
window.setInterval(refreshAlertStatus, 30000);
window.setInterval(refreshDiagnostics, 30000);
