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
  card.classList.remove(...statusOrder);
  card.classList.add(status);
  card.querySelector("h3").textContent = status;
  card.querySelector(".message").textContent = check.message;
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
window.setInterval(refreshHealth, 30000);
