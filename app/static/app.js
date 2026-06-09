const statusClassList = ["healthy", "warning", "degraded", "critical", "unknown", "not-configured"];

const statusLabel = {
  healthy: "健康",
  warning: "警告",
  degraded: "降级",
  critical: "严重",
  unknown: "未知",
  "not-configured": "未配置",
};

const trafficSafeNote = "本地流量估算安全。服务商后台计费可能与本地估算不同。";
const readOnlyDiagnosticsNotice = "以下命令仅用于只读排查，不会自动执行。";

const moduleLabels = {
  vps_system: "VPS 健康",
  proxy_core: "代理核心运行",
  xui_panel: "3X-UI 面板可达",
  proxy_ports: "代理端口开放",
  domain_dns: "域名 / DNS",
  tls_certificate: "TLS 证书",
  traffic: "流量风险",
};

function normalizeStatus(status) {
  return statusClassList.includes(status) ? status : "unknown";
}

function toDisplayStatus(status) {
  return statusLabel[status] || statusLabel.unknown;
}

function setCardState(card, status, isIgnored) {
  card.classList.remove(...statusClassList);
  if (isIgnored) {
    card.classList.add("not-configured");
    return;
  }
  card.classList.add(status);
}

function updateCard(check) {
  const card = document.querySelector(`[data-check="${check.name}"]`);
  if (!card) {
    return;
  }

  const ignored = Boolean(check.ignored);
  const status = normalizeStatus(check.status);
  const displayStatus = ignored ? "not-configured" : status;

  setCardState(card, status, ignored);
  const title = card.querySelector("h3");
  if (title) {
    title.textContent = toDisplayStatus(displayStatus);
  }
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
    const resolvedCount = Object.values(resolved).reduce(
      (count, ips) => count + (Array.isArray(ips) ? ips.length : 0),
      0,
    );
    const hasExpected = Array.isArray(details.expected_ips) && details.expected_ips.length > 0;
    const hasMismatch = Array.isArray(details.mismatches) && details.mismatches.length > 0;
    setDetail(card, "resolved_ip_count", check.ignored ? "未配置" : resolvedCount);
    if (check.ignored || !hasExpected) {
      setDetail(card, "expected_match", "未配置");
    } else if (hasMismatch) {
      setDetail(card, "expected_match", "否");
    } else {
      setDetail(card, "expected_match", "是");
    }
  }

  if (check.name === "tls_certificate") {
    const targets = Array.isArray(details.targets) ? details.targets : [];
    const target = targets[0] || {};
    setDetail(card, "days_remaining", check.ignored ? "未配置" : formatInt(target.days_remaining, "未配置"));
    setDetail(card, "not_after", check.ignored ? "未配置" : formatDate(target.not_after));
  }
}

function formatGb(value) {
  if (typeof value !== "number") {
    return "--";
  }
  return `${value.toFixed(2)} GB`;
}

function formatPercent(value) {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "--";
  }
  if (value === 0) {
    return "0%";
  }
  if (value > 0 && value < 0.1) {
    return "<0.1%";
  }
  return `${value.toFixed(1)}%`;
}

function formatInt(value, fallback) {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return fallback ?? "--";
  }
  return String(Math.trunc(value));
}

function formatDate(value) {
  if (!value) {
    return "--";
  }
  return new Date(value).toLocaleDateString();
}

function localizeReadableSummary(text) {
  if (text === "All configured health checks look healthy. Not configured: domain_dns, tls_certificate.") {
    return "已启用的健康检查均正常。域名 / DNS 与 TLS 证书检查尚未配置。";
  }
  if (text === "No visible risks from current checks.") {
    return "当前没有可见风险。";
  }
  return text || "未获取摘要。";
}

function findCheck(checks, name) {
  return checks.find((item) => item.name === name);
}

function getPipelineState(check) {
  if (!check) {
    return "unknown";
  }
  if (check.ignored) {
    return "ok";
  }
  if (["warning", "degraded", "critical"].includes(check.status)) {
    return "risk";
  }
  if (check.status === "healthy") {
    return "ok";
  }
  return "unknown";
}

function renderPipeline(checks) {
  const vps = findCheck(checks, "vps_system");
  const proxyCore = findCheck(checks, "proxy_core");
  const panel = findCheck(checks, "xui_panel");
  const ports = findCheck(checks, "proxy_ports");

  const stepMap = [
    { id: "pipeline-vps", check: vps },
    { id: "pipeline-proxy-core", check: proxyCore },
    { id: "pipeline-panel", check: panel },
    { id: "pipeline-port", check: ports },
  ];

  let hasRisk = false;

  stepMap.forEach(({ id, check }) => {
    const node = document.getElementById(id);
    if (!node || !check) {
      return;
    }
    const state = getPipelineState(check);
    node.classList.remove("ok", "risk", "unknown");
    if (state === "risk") {
      node.classList.add("risk");
      hasRisk = true;
    } else if (state === "ok") {
      node.classList.add("ok");
    } else {
      node.classList.add("risk");
      hasRisk = true;
    }
  });

  const summary = document.getElementById("pipeline-summary");
  if (!summary) {
    return;
  }
  if (hasRisk) {
    summary.textContent = "代理链路存在风险，请查看诊断建议。";
  } else {
    summary.textContent = "代理链路正常，当前未发现影响代理使用的风险。";
  }
}

function renderRiskAndOptional(checks) {
  const activeRiskChecks = checks.filter(
    (check) => !check.ignored && ["warning", "degraded", "critical"].includes(normalizeStatus(check.status)),
  );
  const riskSummary = document.getElementById("risk-summary");
  if (riskSummary) {
    riskSummary.replaceChildren();
    if (activeRiskChecks.length === 0) {
      const li = document.createElement("li");
      li.textContent = "当前没有活跃风险。";
      riskSummary.appendChild(li);
    } else {
      activeRiskChecks.forEach((check) => {
        const li = document.createElement("li");
        const label = moduleLabels[check.name] || check.name;
        li.textContent = `${label}：${check.message}`;
        riskSummary.appendChild(li);
      });
    }
  }

  const optionalChecks = document.getElementById("optional-checks");
  if (optionalChecks) {
    optionalChecks.setAttribute("aria-label", "未配置的可选检查");
    optionalChecks.replaceChildren();
    const optionalNames = ["domain_dns", "tls_certificate"];
    optionalNames.forEach((name) => {
      const check = checks.find((item) => item.name === name);
      const label = moduleLabels[name] || name;
      const li = document.createElement("li");
      li.textContent = `${label}：${check && check.ignored ? "未配置" : (check ? "已配置" : "未知")}`;
      optionalChecks.appendChild(li);
    });
  }
}

function renderHealth(data) {
  const checks = Array.isArray(data.checks) ? data.checks : [];
  const overallStatus = normalizeStatus(data.overall_status);
  const badge = document.getElementById("overall-badge");
  badge.classList.remove(...statusClassList);
  badge.classList.add(overallStatus);
  badge.textContent = toDisplayStatus(overallStatus);

  document.getElementById("overall-status").textContent = `总体状态：${toDisplayStatus(overallStatus)}`;
  document.getElementById("readable-summary").textContent = localizeReadableSummary(data.readable_summary);
  document.getElementById("last-checked").textContent = `最后检查：${new Date(data.checked_at).toLocaleString()}`;

  checks.forEach(updateCard);
  renderPipeline(checks);
  renderRiskAndOptional(checks);
}

function renderManagement(data) {
  const status = data.enabled === false ? "not-configured" : normalizeStatus(data.status);
  const title = document.getElementById("management-status");
  const button = document.getElementById("management-open-button");
  const publicUrl = data.panel_public_url || "";

  title.textContent = data.enabled === false ? "已关闭" : toDisplayStatus(status);
  document.getElementById("management-message").textContent = data.message || "管理入口状态暂不可用。";
  document.getElementById("management-panel-name").textContent = data.panel_name || "3X-UI 面板";
  document.getElementById("management-local-url").textContent = data.panel_local_url || "--";
  document.getElementById("management-public-url").textContent = publicUrl || "未配置";
  document.getElementById("management-access-note").textContent =
    data.access_note || "建议通过 Cloudflare Access + 3X-UI 登录双层保护访问。";
  document.getElementById("management-readonly-note").textContent =
    data.readonly_note || "Control Tower 不读取或修改 3X-UI 配置。";

  if (publicUrl) {
    button.href = publicUrl;
    button.setAttribute("aria-disabled", "false");
    button.classList.remove("disabled");
    button.textContent = "进入 3X-UI 面板";
    button.target = data.open_in_new_tab === false ? "_self" : "_blank";
  } else {
    button.removeAttribute("href");
    button.setAttribute("aria-disabled", "true");
    button.classList.add("disabled");
    button.textContent = "请先配置 panel_public_url";
  }
}

async function refreshManagement() {
  try {
    const response = await fetch("/api/management", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderManagement(await response.json());
  } catch (error) {
    renderManagement({
      enabled: true,
      status: "unknown",
      message: `管理入口不可用：${error.message}`,
      panel_name: "3X-UI 面板",
      panel_local_url: "--",
      panel_public_url: "",
      access_note: "建议通过 Cloudflare Access + 3X-UI 登录双层保护访问。",
      readonly_note: "Control Tower 不读取或修改 3X-UI 配置。",
      open_in_new_tab: true,
    });
  }
}

function renderAlertStatus(data) {
  const alerts = data.alerts || {};
  const telegram = data.telegram || {};
  const email = data.email || {};
  const state = data.state || {};

  const alertsEnabled = !!alerts.enabled;
  document.getElementById("alerts-enabled").textContent = alertsEnabled ? "已开启" : "已关闭";
  document.getElementById("alerts-message").textContent = alertsEnabled
    ? "已开启告警，达到配置阈值时发送通知。"
    : "告警已关闭，不会发送通知。";

  document.getElementById("alerts-min-severity").textContent = alerts.min_severity || "--";
  document.getElementById("alerts-cooldown").textContent = `${alerts.cooldown_seconds ?? "--"}s`;
  document.getElementById("alerts-telegram").textContent = telegram.enabled ? "已开启" : "已关闭";
  document.getElementById("alerts-email").textContent = email.enabled ? "已开启" : "已关闭";
  document.getElementById("alerts-active").textContent = state.active_alert_count ?? "--";
  document.getElementById("alerts-last-sent").textContent = state.last_sent_at
    ? new Date(state.last_sent_at).toLocaleString()
    : "--";

  const badge = document.getElementById("alerts-enabled");
  badge.classList.remove(...statusClassList);
  badge.classList.add(alertsEnabled ? "healthy" : "not-configured");
}

function renderAlertConfigCheck(data) {
  const configMessageEl = document.getElementById("alerts-config-message");
  const configStateEl = document.getElementById("alerts-config-state");
  const safeToTestEl = document.getElementById("alerts-safe-to-test");
  const recoveryEl = document.getElementById("alerts-recovery");
  const telegramEl = document.getElementById("alerts-telegram");
  const emailEl = document.getElementById("alerts-email");
  const telegram = data.channels?.telegram || {};
  const email = data.channels?.email || {};

  configMessageEl.textContent = data.message || "告警配置读取失败，请稍后再试。";
  recoveryEl.textContent = String(data.send_recovery ?? "--");
  safeToTestEl.textContent = data.safe_to_test ? "可以" : "不可以";
  configStateEl.textContent = data.status === "healthy" ? "就绪" : "未就绪";

  if (telegramEl) {
    if (telegram.enabled) {
      telegramEl.textContent = telegram.ready
        ? "已开启且配置完整"
        : "已开启但配置不完整";
    } else {
      telegramEl.textContent = "未开启";
    }
  }

  if (emailEl) {
    if (email.enabled) {
      emailEl.textContent = email.ready
        ? "已开启且配置完整"
        : "已开启但配置不完整";
    } else {
      emailEl.textContent = "未开启";
    }
  }
}

async function refreshAlertStatus() {
  try {
    const response = await fetch("/api/alerts/status", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderAlertStatus(await response.json());
  } catch (error) {
    document.getElementById("alerts-message").textContent = `告警状态不可用：${error.message}`;
  }
}

function renderMeta(meta) {
  const accessHint = meta.access_hint || "SSH Tunnel";
  const host = meta.configured_host || "127.0.0.1";
  const port = meta.configured_port || 3001;
  const mode = meta.local_only ? "本地只读" : "未知模式";

  const runtimeBar = document.getElementById("runtime-bar");
  if (runtimeBar) {
    runtimeBar.textContent = `${mode} · 绑定：${host}:${port} · 访问方式：${accessHint} · 公网暴露：无`;
  }

  document.getElementById("runtime-mode").textContent = mode;
  document.getElementById("runtime-endpoint").textContent = `${host}:${port}`;
  document.getElementById("runtime-access").textContent = accessHint;
}

function setDiagnosticsVisibility(item, dataSummary) {
  const summary = document.getElementById("diagnostics-summary");
  const titleEl = document.querySelector("#top-diagnosis h3");
  const impactEl = document.getElementById("diagnosis-impact");
  const firstCheckEl = document.getElementById("diagnosis-first-check");
  const relatedEl = document.getElementById("diagnosis-related");
  const confidenceEl = document.getElementById("diagnosis-confidence");
  const commandsEl = document.getElementById("diagnosis-commands");

  if (!item) {
    summary.textContent = "未发现需要处理的诊断问题。";
    titleEl.textContent = "未发现需要处理的诊断问题。";
    impactEl.textContent = "当前无需执行排查命令。";
    firstCheckEl.textContent = "";
    relatedEl.textContent = "";
    confidenceEl.textContent = "置信度：高";
    commandsEl.textContent = "暂无命令。";
    return;
  }

  const title = `${item.title}（${toDisplayStatus(normalizeStatus(item.status))}）`;
  summary.textContent = `${dataSummary || "存在诊断项。"}：${item.title}`;
  titleEl.textContent = title;
  impactEl.textContent = `影响：${item.impact || "--"}`;
  firstCheckEl.textContent = `建议先做：${item.suggested_first_check || "--"}`;
  const relatedModules = (item.related_modules || []).join("、");
  relatedEl.textContent = `相关模块：${relatedModules || "--"}`;
  confidenceEl.textContent = `置信度：${item.confidence || "--"}`;
  const commands = Array.isArray(item.read_only_commands) ? item.read_only_commands : [];
  if (commands.length) {
    commandsEl.textContent = `${readOnlyDiagnosticsNotice}\n如需修改代理配置，可通过“管理入口”进入 3X-UI 面板。\n${commands.join("\n")}`;
  } else {
    commandsEl.textContent = `${readOnlyDiagnosticsNotice}\n暂无命令。`;
  }
}

function renderDiagnosticsSummary(data) {
  const first = Array.isArray(data.items) ? data.items[0] : null;
  if (!first) {
    setDiagnosticsVisibility(null, data.summary);
    return;
  }
  setDiagnosticsVisibility(first, data.summary);
}

async function refreshDiagnostics() {
  try {
    const response = await fetch("/api/diagnostics", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    renderDiagnosticsSummary(data);
  } catch (error) {
    const summary = document.getElementById("diagnostics-summary");
    summary.textContent = `诊断不可用：${error.message}`;
    setDiagnosticsVisibility(null);
  }
}

function renderHistory(summary, events) {
  const statusEl = document.getElementById("history-status");
  const currentEl = document.getElementById("history-current-status");
  const worstEl = document.getElementById("history-worst-status");
  const ratioEl = document.getElementById("history-health-ratio");
  const snapshotCountEl = document.getElementById("history-snapshot-count");
  const eventCountEl = document.getElementById("history-event-count");
  const lastProblemEl = document.getElementById("history-last-problem");
  const lastRecoveryEl = document.getElementById("history-last-recovery");
  const listEl = document.getElementById("history-events-list");
  const summaryEl = document.getElementById("history-summary");

  if (!summary || !summary.enabled) {
    summaryEl.textContent = "健康历史记录已关闭。";
    statusEl.textContent = "--";
    currentEl.textContent = "--";
    worstEl.textContent = "--";
    ratioEl.textContent = "--";
    snapshotCountEl.textContent = "0";
    eventCountEl.textContent = "0";
    lastProblemEl.textContent = "--";
    lastRecoveryEl.textContent = "--";
    listEl.replaceChildren();
    const li = document.createElement("li");
    li.textContent = "健康历史已关闭。";
    listEl.appendChild(li);
    return;
  }

  summaryEl.textContent = summary.summary || "暂无历史摘要。";
  statusEl.textContent = summary.status || "--";
  currentEl.textContent = summary.latest_status || "--";
  worstEl.textContent = summary.worst_status || "--";
  ratioEl.textContent = typeof summary.healthy_ratio === "number" ? `${summary.healthy_ratio.toFixed(1)}%` : "--";
  snapshotCountEl.textContent = `${summary.snapshot_count || 0}`;
  eventCountEl.textContent = `${summary.event_count || 0}`;
  lastProblemEl.textContent = summary.last_problem_at || "--";
  lastRecoveryEl.textContent = summary.last_recovery_at || "--";

  const visibleEvents = Array.isArray(events) ? events.slice(-5) : [];
  listEl.replaceChildren();
  if (visibleEvents.length === 0) {
    const li = document.createElement("li");
    li.textContent = "未发现最近可展示的历史事件。";
    listEl.appendChild(li);
    return;
  }

  visibleEvents.forEach((item) => {
    const li = document.createElement("li");
    const time = item.occurred_at ? new Date(item.occurred_at).toLocaleString() : "--";
    li.textContent = `${time} ${item.title || item.message || "未命名事件"}`;
    listEl.appendChild(li);
  });
}

async function refreshHistory() {
  try {
    const [summaryResp, recentResp, eventsResp] = await Promise.all([
      fetch("/api/history/summary", { cache: "no-store" }),
      fetch("/api/history/recent?limit=50", { cache: "no-store" }),
      fetch("/api/events?limit=50", { cache: "no-store" }),
    ]);
    if (!summaryResp.ok || !recentResp.ok || !eventsResp.ok) {
      throw new Error(`HTTP ${summaryResp.status || recentResp.status || eventsResp.status}`);
    }
    const summary = await summaryResp.json();
    const events = await eventsResp.json();
    renderHistory(summary, events.items || []);
  } catch (error) {
    const summaryEl = document.getElementById("history-summary");
    summaryEl.textContent = `历史数据暂不可用，请查看服务日志：${error.message}`;
  }
}

async function sendTestAlert() {
  const output = document.getElementById("test-alert-result");
  output.textContent = "正在发送测试告警...";
  try {
    const response = await fetch("/api/alerts/test", { method: "POST" });
    const data = await response.json();
    if (data.sent) {
      output.textContent = "测试告警已发送。";
    } else if (typeof data.message === "string" && data.message.length > 0) {
      output.textContent = `测试告警已跳过：${data.message}`;
    } else {
      output.textContent = "测试告警已跳过。";
    }
    await refreshAlertStatus();
    await refreshAlertConfigCheck();
  } catch (error) {
    output.textContent = `测试告警失败：${error.message}`;
  }
}

async function refreshMeta() {
  try {
    const response = await fetch("/api/meta", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderMeta(await response.json());
  } catch (error) {
    const fallback = "本地只读 · 绑定：127.0.0.1:3001 · 访问方式：SSH Tunnel · 公网暴露：无";
    document.getElementById("runtime-bar").textContent = fallback;
    document.getElementById("runtime-access").textContent = "SSH Tunnel";
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
      readable_summary: "面板无法从本地 API 读取健康数据。",
      checked_at: new Date().toISOString(),
      risk_summary: [`api: ${error.message}`],
      checks: [],
      history_recording: { recorded: false, reason: error.message },
    });
  }
}

async function refreshAlertConfigCheck() {
  try {
    const response = await fetch("/api/alerts/config-check", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    renderAlertConfigCheck(data);
  } catch (error) {
    const msg = document.getElementById("alerts-config-message");
    if (msg) {
      msg.textContent = `告警配置校验不可用：${error.message}`;
    }
    const state = document.getElementById("alerts-config-state");
    if (state) {
      state.textContent = "未知";
    }
  }
}

refreshMeta();
refreshHealth();
refreshManagement();
refreshAlertStatus();
refreshAlertConfigCheck();
refreshDiagnostics();
refreshHistory();
document.getElementById("test-alert-button").addEventListener("click", sendTestAlert);
window.setInterval(refreshHealth, 30000);
window.setInterval(refreshManagement, 60000);
window.setInterval(refreshAlertStatus, 30000);
window.setInterval(refreshAlertConfigCheck, 60000);
window.setInterval(refreshDiagnostics, 30000);
window.setInterval(refreshHistory, 60000);
