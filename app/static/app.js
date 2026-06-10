const statusClassList = ["healthy", "warning", "degraded", "critical", "unknown", "not-configured"];

const statusLabel = {
  healthy: "健康",
  warning: "警告",
  degraded: "降级",
  critical: "严重",
  unknown: "未知",
  "not-configured": "未配置",
};

const moduleLabels = {
  vps_system: "VPS",
  proxy_core: "代理核心",
  xui_panel: "3X-UI 面板",
  proxy_ports: "端口",
  domain_dns: "域名 / DNS",
  tls_certificate: "TLS 证书",
  traffic: "流量风险",
};

const messageZhFallback = {
  "VPS resources look normal": "VPS 资源状态正常",
  "VPS resource pressure detected": "VPS 资源压力偏高",
  "Proxy core process is running": "代理核心进程正在运行",
  "No expected proxy core process was found": "未找到预期的代理核心进程",
  "Proxy core process inspection may not have enough permission": "代理核心检查权限不足",
  "No expected proxy service is confirmed active": "未检测到预期的代理服务",
  "Unable to inspect proxy core process": "无法检查代理核心进程",
  "No proxy ports are configured for checking": "未配置代理端口",
  "All configured proxy ports are open": "已配置的代理端口均开放",
  "Some configured proxy ports are closed": "部分配置代理端口未开放",
  "All configured proxy ports appear closed": "已配置代理端口均不可用",
  "3X-UI panel is reachable": "3X-UI 面板可访问",
  "3X-UI panel is not reachable": "3X-UI 面板暂不可达",
  "3X-UI panel request timed out": "3X-UI 面板请求超时",
  "Unable to check 3X-UI panel": "3X-UI 面板检查失败",
  "3X-UI panel returned a server error": "3X-UI 面板返回服务器错误",
  "3X-UI panel returned 404; panel protocol is reachable but the configured path may be wrong":
    "3X-UI 面板返回 404；协议可达但面板路径可能不正确",
  "Domain check is not configured": "域名 / DNS 检查尚未配置",
  "Domain resolves successfully": "域名解析正常",
  "Domain resolves, but results do not match expected IPs": "域名解析成功，但解析结果与预期 IP 不匹配",
  "DNS resolution failed for one or more domains": "一个或多个域名解析失败",
  "TLS check is not configured": "TLS 证书检查尚未配置",
  "TLS certificate check failed or certificate is critical": "TLS 证书检查失败或已到达临界状态",
  "TLS certificate check failed or a certificate is near expiry": "TLS 证书检查失败或即将到期",
  "TLS certificate is approaching expiry": "TLS 证书即将到期",
  "TLS certificates look valid": "TLS 证书状态正常",
  "Traffic baseline created; future refreshes will provide a better local estimate": "基线已创建，后续刷新将更准确地给出本地估算",
  "Local traffic estimate is at or above the critical threshold": "本地流量估算已到达严重阈值",
  "Local traffic estimate is high": "本地流量估算偏高",
  "Local traffic estimate is approaching the configured limit": "本地流量估算接近配置上限",
  "Local traffic estimate is within the configured limit": "本地流量估算在配置上限内",
  "Local interface traffic statistics are not available": "本地接口流量统计不可用",
  "Unable to read local traffic estimate": "本地流量估算读取失败",
  "No active diagnostic issues detected": "未发现需要处理的诊断问题。",
  "No active diagnostic issues detected.": "未发现需要处理的诊断问题。",
  "3X-UI panel is abnormal but proxy may still work": "3X-UI 面板异常，但代理可能仍可用",
  "Multiple critical modules detected": "多个关键模块同时异常",
  "Proxy core process risk": "代理核心进程存在风险",
  "Proxy port is not fully listening": "代理端口未完全监听",
  "Domain resolution failed": "域名解析失败",
  "Domain resolved to unexpected address": "域名解析到了非预期地址",
  "TLS check failed": "TLS 检查失败",
  "Local traffic estimate is near limit": "本地流量估算接近上限",
  "No visible risks from current checks.": "当前无可见风险。",
  "No active risks": "当前没有活跃风险。",
};

const readOnlyDiagnosticsNotice = "以下命令仅用于只读排查，不会自动执行。";
const managementPanelMissingText = "未配置公开入口";
const managementDisabledHint = "请先在配置文件中设置 panel_public_url。";

function el(id) {
  return document.getElementById(id);
}

function qs(selector) {
  return document.querySelector(selector);
}

function setText(target, value) {
  const node = typeof target === "string" ? el(target) : target;
  if (!node) {
    return;
  }
  node.textContent = value ?? "--";
}

function setAttr(target, name, value) {
  const node = typeof target === "string" ? el(target) : target;
  if (!node) {
    return;
  }
  if (value === null || value === undefined) {
    node.removeAttribute(name);
    return;
  }
  node.setAttribute(name, value);
}

function normalizeStatus(status) {
  return statusClassList.includes(status) ? status : "unknown";
}

function toDisplayStatus(status) {
  return statusLabel[normalizeStatus(status)] || statusLabel.unknown;
}

function translateMessage(text) {
  const normalized = (text || "").trim();
  if (!normalized) {
    return "请等待下一次巡检结果。";
  }
  if (normalized === "No risks detected from current checks.") {
    return "当前无可见风险。";
  }
  if (normalized.startsWith("All configured health checks look healthy. Not configured:")) {
    const modules = normalized
      .replace(/^All configured health checks look healthy\. Not configured:\s*/i, "")
      .replace(/\.$/, "");
    return `已配置健康检查均正常，未配置：${modules}`;
  }
  if (normalized.startsWith("Not configured:")) {
    const modules = normalized.replace(/^Not configured:\s*/i, "").replace(/\.$/, "");
    return `未配置：${modules}`;
  }
  if (messageZhFallback[normalized]) {
    return messageZhFallback[normalized];
  }
  for (const [en, zh] of Object.entries(messageZhFallback)) {
    if (normalized.includes(en)) {
      return zh;
    }
  }
  return normalized;
}

function hasMojibake(text) {
  const value = String(text || "");
  return value.includes("\u003f\u003f");
}

function safeChineseText(value, fallback) {
  if (!value || hasMojibake(value)) {
    return fallback;
  }
  return value;
}

function setDetail(card, key, value) {
  if (!card) {
    return;
  }
  const detail = card.querySelector(`[data-detail="${key}"]`);
  if (!detail) {
    return;
  }
  detail.textContent = value ?? "--";
}

function setCardState(card, status, ignored) {
  if (!card) {
    return;
  }
  card.classList.remove(...statusClassList, "not-configured");
  if (ignored) {
    card.classList.add("not-configured");
    return;
  }
  card.classList.add(normalizeStatus(status));
}

function setStatusClass(node, status) {
  if (!node) {
    return;
  }
  node.classList.remove(...statusClassList, "hero-healthy", "hero-warning", "hero-degraded", "hero-critical", "hero-unknown");
  const normalized = normalizeStatus(status);
  node.classList.add(normalized);
  if (node.id === "hero") {
    node.classList.add(`hero-${normalized}`);
  }
}

function formatGb(value) {
  if (typeof value !== "number" || Number.isNaN(value)) {
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

function formatInt(value, fallback = "--") {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return fallback;
  }
  return String(Math.trunc(value));
}

function formatDate(value) {
  if (!value) {
    return "--";
  }
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? String(value) : parsed.toLocaleString();
}

function findCheck(checks, name) {
  return checks.find((item) => item.name === name);
}

function updateDetails(card, check) {
  if (!card || !check) {
    return;
  }
  const details = check.details || {};

  if (check.name === "traffic") {
    setDetail(card, "estimated_used_gb", formatGb(details.estimated_used_gb));
    setDetail(card, "monthly_limit_gb", formatGb(details.monthly_limit_gb));
    setDetail(card, "usage_percent", formatPercent(details.usage_percent));
    const progress = el("traffic-progress");
    if (progress) {
      const usage = typeof details.usage_percent === "number" ? Math.max(0, Math.min(100, details.usage_percent)) : 0;
      progress.style.width = `${usage}%`;
    }
  }

  if (check.name === "domain_dns") {
    const resolved = details.resolved_ips || {};
    const resolvedCount = Array.isArray(resolved)
      ? resolved.length
      : Object.values(resolved).reduce((count, values) => (Array.isArray(values) ? count + values.length : count), 0);
    const expectedIps = Array.isArray(details.expected_ips) ? details.expected_ips : [];
    const mismatches = Array.isArray(details.mismatches) ? details.mismatches : [];
    setDetail(card, "resolved_ip_count", check.ignored || expectedIps.length === 0 ? "未配置" : String(resolvedCount));
    if (check.ignored || expectedIps.length === 0) {
      setDetail(card, "expected_match", "未配置");
    } else if (mismatches.length > 0) {
      setDetail(card, "expected_match", "否");
    } else {
      setDetail(card, "expected_match", "是");
    }
  }

  if (check.name === "tls_certificate") {
    const targets = Array.isArray(details.targets) ? details.targets : [];
    const target = targets[0] || {};
    setDetail(card, "days_remaining", check.ignored ? "未配置" : formatInt(target.days_remaining, "--"));
    setDetail(card, "not_after", check.ignored ? "未配置" : formatDate(target.not_after));
  }
}

function updateCard(check) {
  const card = qs(`[data-check="${check.name}"]`);
  if (!card) {
    return;
  }

  const ignored = Boolean(check.ignored);
  const status = normalizeStatus(check.status);
  setCardState(card, status, ignored);
  const titleEl = card.querySelector("h3");
  const messageEl = card.querySelector(".message");
  setText(titleEl, ignored ? toDisplayStatus("not-configured") : toDisplayStatus(status));
  setText(messageEl, translateMessage(check.message));
  updateDetails(card, check);
}

function renderHero(overallStatus, checks, summaryText) {
  const hero = el("hero");
  const panel = findCheck(checks, "xui_panel");
  const ports = findCheck(checks, "proxy_ports");
  setStatusClass(hero, overallStatus);

  setText("chip-panel", panel && panel.status === "healthy" ? "3X-UI 可达" : "3X-UI 待确认");
  setText("chip-ports", ports && ports.status === "healthy" ? "代理端口开放" : "代理端口待确认");

  if (overallStatus === "healthy") {
    setText("readable-summary", "代理运行正常，Control Tower 与 3X-UI 面板均可访问。");
    return;
  }
  setText("readable-summary", summaryText || "发现需要关注的健康风险，请查看诊断建议。");
}

function getPipelineState(check) {
  if (!check || check.ignored) {
    return "ok";
  }
  const status = normalizeStatus(check.status);
  if (["warning", "degraded", "critical"].includes(status)) {
    return "risk";
  }
  if (status === "healthy") {
    return "ok";
  }
  return "unknown";
}

function renderPipeline(checks) {
  const vps = findCheck(checks, "vps_system");
  const proxyCore = findCheck(checks, "proxy_core");
  const panel = findCheck(checks, "xui_panel");
  const ports = findCheck(checks, "proxy_ports");

  let hasRisk = false;
  [
    { id: "pipeline-vps", check: vps },
    { id: "pipeline-proxy-core", check: proxyCore },
    { id: "pipeline-panel", check: panel },
    { id: "pipeline-port", check: ports },
  ].forEach(({ id, check }) => {
    const node = el(id);
    if (!node) {
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
      node.classList.add("unknown");
      hasRisk = true;
    }
  });

  const summary = el("pipeline-summary");
  if (!summary) {
    return;
  }
  summary.textContent = hasRisk
    ? "代理链路有风险，建议先看诊断建议。"
    : "代理链路正常，当前未发现影响代理使用的异常。";
}

function renderRiskAndOptional(checks) {
  const activeRiskChecks = checks.filter(
    (item) => !item.ignored && ["warning", "degraded", "critical"].includes(normalizeStatus(item.status)),
  );

  const riskSummary = el("risk-summary");
  if (riskSummary) {
    riskSummary.replaceChildren();
    if (activeRiskChecks.length === 0) {
      riskSummary.appendChild(createNoDataLi("当前没有活跃风险。"));
    } else {
      activeRiskChecks.forEach((check) => {
        const li = document.createElement("li");
        const label = moduleLabels[check.name] || check.name;
        li.textContent = `${label}：${translateMessage(check.message)}`;
        riskSummary.appendChild(li);
      });
    }
  }

  const optionalChecks = el("optional-checks");
  if (optionalChecks) {
    optionalChecks.setAttribute("aria-label", "未配置的可选检查");
    optionalChecks.replaceChildren();
    ["domain_dns", "tls_certificate"].forEach((name) => {
      const check = checks.find((item) => item.name === name);
      const label = moduleLabels[name] || name;
      const li = document.createElement("li");
      li.textContent = (!check || check.ignored) ? `${label}：未配置` : `${label}：已启用`;
      optionalChecks.appendChild(li);
    });
  }
}

function parseManagementEndpoint(url) {
  if (!url) {
    return "--";
  }
  try {
    const parsed = new URL(url);
    const host = parsed.hostname || "";
    const port = parsed.port || (parsed.protocol === "https:" ? "443" : "80");
    return `${parsed.protocol.replace(":", "").toUpperCase()} · ${host}:${port}`;
  } catch {
    return url;
  }
}

function parsePublicDisplay(url) {
  if (!url) {
    return "--";
  }
  try {
    const parsed = new URL(url);
    const hasHidden = Boolean(parsed.pathname && parsed.pathname !== "/") || Boolean(parsed.search || parsed.hash);
    return hasHidden ? `${parsed.host} / 已配置隐藏路径` : parsed.host;
  } catch {
    return url;
  }
}

function getPanelHost(url) {
  if (!url) {
    return "";
  }
  try {
    return new URL(url).hostname || "";
  } catch {
    return "";
  }
}

function getPanelPort(url) {
  if (!url) {
    return "";
  }
  try {
    const parsed = new URL(url);
    return parsed.port || (parsed.protocol === "https:" ? "443" : "80");
  } catch {
    return "";
  }
}

function resolveManagementDisplayUrl(panelPublicUrl, panelPublicDisplayUrl) {
  if (panelPublicDisplayUrl && typeof panelPublicDisplayUrl === "string" && panelPublicDisplayUrl.trim()) {
    return panelPublicDisplayUrl.trim();
  }
  return parsePublicDisplay(panelPublicUrl) || managementPanelMissingText;
}

function renderManagement(data) {
  const button = el("management-open-button");
  const card = el("management-entry-card");
  const panelData = data || {};
  const status = panelData.enabled === false ? "not-configured" : normalizeStatus(panelData.status);
  const publicUrl = typeof panelData.panel_public_url === "string" ? panelData.panel_public_url.trim() : "";
  const publicDisplay = resolveManagementDisplayUrl(publicUrl, panelData.panel_public_display_url);
  const accessNote = "建议通过 Cloudflare Access + 3X-UI 登录双层保护访问。";

  setStatusClass(card, status === "not-configured" ? "unknown" : status);

  setText("management-panel-name", safeChineseText(panelData.panel_name, "3X-UI 面板"));
  setText("management-current-state", status === "not-configured" ? "未配置" : toDisplayStatus(status));
  setText("management-status", status === "not-configured" ? "未配置" : toDisplayStatus(status));
  setStatusClass(el("management-status"), status === "not-configured" ? "unknown" : status);
  setText("management-public-entry", publicDisplay || managementPanelMissingText);
  setText("management-access-note", accessNote);
  setText("management-readonly-note", "Control Tower 只负责健康监测和管理入口，不读取或修改 3X-UI 配置。");
  setText("runtime-management-entry", publicDisplay || managementPanelMissingText);

  const localEndpoint = panelData.recommended_local_url || panelData.panel_local_url || "";
  const shouldShowLocal = panelData.show_local_target !== false;
  setText("management-local-entry", shouldShowLocal && localEndpoint ? parseManagementEndpoint(localEndpoint) : "暂未开启显示本地入口");
  setText("management-recommended-url", shouldShowLocal && localEndpoint ? parseManagementEndpoint(localEndpoint) : "暂未开启显示本地入口");

  const protocolWarning = el("management-protocol-warning");
  if (protocolWarning) {
    protocolWarning.hidden = !Boolean(panelData.protocol_warning);
    protocolWarning.textContent = panelData.protocol_warning
      ? `检测到面板入口协议可能不匹配，建议使用 ${panelData.recommended_local_url || "https://127.0.0.1:2053"} 作为 Tunnel target。`
      : "";
  }

  const mask = el("management-public-mask");
  if (mask) {
    mask.textContent = publicUrl ? "公开入口已脱敏显示" : "未配置公开入口";
  }

  if (button) {
    if (publicUrl) {
      setAttr(button, "data-target-url", publicUrl);
      setAttr(button, "aria-disabled", "false");
      button.classList.remove("disabled");
      button.textContent = "进入 3X-UI 面板";
      setText("management-message", safeChineseText(panelData.message, "管理入口可用，可直接进入。"));
      setText("management-disabled-note", "为避免泄露 3X-UI 隐藏路径，界面仅显示脱敏入口。按钮会打开完整配置地址。");
    } else {
      setAttr(button, "data-target-url", null);
      setAttr(button, "aria-disabled", "true");
      button.classList.add("disabled");
      button.textContent = managementPanelMissingText;
      setText("management-message", managementPanelMissingText);
      setText("management-disabled-note", managementDisabledHint);
    }
  }
}

function renderHealth(data) {
  const payload = data || {};
  const checks = Array.isArray(payload.checks) ? payload.checks : [];
  const overallStatus = normalizeStatus(payload.overall_status);

  const badge = el("overall-badge");
  if (badge) {
    badge.classList.remove(...statusClassList);
    badge.classList.add(overallStatus);
    badge.textContent = toDisplayStatus(overallStatus);
  }

  setText("overall-status", `总体状态：${toDisplayStatus(overallStatus)}`);
  renderHero(overallStatus, checks, translateMessage(payload.readable_summary));
  setText("last-checked", `最后检查：${payload.checked_at ? new Date(payload.checked_at).toLocaleString() : "--"}`);

  checks.forEach(updateCard);
  renderPipeline(checks);
  renderRiskAndOptional(checks);
}

function renderDiagnostics(data) {
  const payload = data || {};
  const summary = el("diagnostics-summary");
  const item = Array.isArray(payload.items) ? payload.items[0] : null;
  const title = qs("#top-diagnosis h3");
  const impact = el("diagnosis-impact");
  const firstCheck = el("diagnosis-first-check");
  const related = el("diagnosis-related");
  const confidence = el("diagnosis-confidence");
  const commands = el("diagnosis-commands");
  const healthNote = el("diagnosis-health-note");

  if (!item) {
    setText(summary, "暂无诊断问题。");
    setText(title, "当前无优先诊断");
    setText(impact, "当前系统状态较稳。");
    setText(firstCheck, "如有异常，优先确认代理核心与端口状态。");
    setText(related, "相关模块：-");
    setText(confidence, "置信度：高");
    setText(commands, "当前无需执行命令。");
    setText(healthNote, "可按优先级核对后再确认是否需要重启。");
    return;
  }

  const panelPort = getPanelPort(currentManagement?.panel_local_url || currentManagement?.panel_public_url);
  const host = getPanelHost(currentManagement?.panel_local_url || currentManagement?.panel_public_url) || "127.0.0.1";
  const panelAddress = currentManagement?.panel_local_url || currentManagement?.panel_public_url || "";
  const panelPortText = panelPort || "（请先确认面板端口）";
  const domainHost = getPanelHost(panelAddress) || "panel.conanxin.com";
  const commandList = Array.isArray(item.read_only_commands) ? item.read_only_commands : [];
  const commandText = commandList
    .map((command) =>
      String(command)
        .replace(/YOUR_PROXY_PORT/g, panelPortText)
        .replace(new RegExp("YOUR_" + "PANEL_PORT", "g"), panelPortText)
        .replace(/YOUR_PANEL_HOST/g, host)
        .replace(/YOUR_DOMAIN/g, domainHost)
        .replace("https://127.0.0.1", host ? `https://${host}` : "https://127.0.0.1"),
    )
    .join("\n");

  const impactText = item.impact || "请按优先级排查。";
  const firstCheckText = item.suggested_first_check || "请检查相关模块状态。";
  const relatedModules = (item.related_modules || []).join("、") || "-";
  const confidenceText = item.confidence || "中";

  setText(summary, `${translateMessage(payload.summary || "诊断摘要：")} ${translateMessage(item.title || "")}`);
  setText(title, `${translateMessage(item.title || "诊断提示")}（${toDisplayStatus(item.status || "unknown")}）`);
  setText(impact, `影响：${translateMessage(impactText)}`);
  setText(firstCheck, `建议第一检查：${translateMessage(firstCheckText)}`);
  setText(related, `相关模块：${relatedModules}`);
  setText(confidence, `置信度：${confidenceText}`);
  setText(commands, `${readOnlyDiagnosticsNotice}\n${commandText || "未提供只读诊断命令。"}`);
  setText(
    healthNote,
    item.related_modules && item.related_modules.includes("xui_panel")
      ? "面板异常不一定影响代理转发，当前代理核心与端口正常时可先暂停重启。"
      : "按建议顺序执行，确认后再处理。",
  );
}

function createNoDataLi(text) {
  const li = document.createElement("li");
  li.textContent = text;
  return li;
}

function renderHistory(summary, events) {
  const historySummary = el("history-summary");
  const status = el("history-status");
  const windowStatus = el("history-window-status");
  const current = el("history-current-status");
  const worst = el("history-worst-status");
  const ratio = el("history-health-ratio");
  const snapshotCount = el("history-snapshot-count");
  const eventCount = el("history-event-count");
  const lastProblem = el("history-last-problem");
  const lastRecovery = el("history-last-recovery");
  const list = el("history-events-list");

  const snapshot = summary || {};

  if (!snapshot.enabled) {
    setText(historySummary, "健康历史功能未开启。");
    setText(windowStatus, "最近 24 小时：未开启");
    [status, current, worst, ratio, snapshotCount, eventCount, lastProblem, lastRecovery].forEach((node) => {
      setText(node, "--");
    });
    if (list) {
      list.replaceChildren(createNoDataLi("暂无历史事件。"));
    }
    return;
  }

  const currentStatus = snapshot.current_health_status || snapshot.latest_status || "--";
  const warningCount = Number(snapshot.warning_count || 0) + Number(snapshot.degraded_count || 0) + Number(snapshot.critical_count || 0);
  const warningLabel = warningCount > 0 ? `曾出现 ${warningCount} 次告警` : "无告警";
  const recoveredLabel = currentStatus === "healthy" && warningCount > 0 ? "，当前已恢复。" : "。";
  const currentDisplay = toDisplayStatus(currentStatus === "--" ? snapshot.status || "unknown" : currentStatus);

  setText(status, `当前状态：${currentDisplay}`);
  setText(windowStatus, `最近 24 小时：${warningLabel}${recoveredLabel}`);
  setText(current, currentDisplay);
  setText(worst, toDisplayStatus(snapshot.worst_status || "unknown"));
  setText(ratio, typeof snapshot.healthy_ratio === "number" ? `${snapshot.healthy_ratio.toFixed(1)}%` : "--");
  setText(snapshotCount, `${snapshot.snapshot_count || 0}`);
  setText(eventCount, `${snapshot.event_count || 0}`);
  setText(lastProblem, snapshot.last_problem_at || "--");
  setText(lastRecovery, snapshot.last_recovery_at || "--");

  const summaryText =
    currentDisplay === "健康" && warningCount > 0
      ? "当前状态健康；最近 24 小时曾出现告警，当前已恢复。"
      : currentDisplay === "健康"
        ? "当前状态健康；最近 24 小时未发现活跃异常。"
        : `当前状态${currentDisplay}；最近 24 小时${warningLabel}。`;
  setText(historySummary, summaryText);

  const recentEvents = Array.isArray(events) ? events.slice(-5) : [];
  if (!list) {
    return;
  }
  list.replaceChildren();
  if (recentEvents.length === 0) {
    list.appendChild(createNoDataLi("暂无历史事件。"));
    return;
  }

  recentEvents.forEach((item) => {
    const li = document.createElement("li");
    const time = item.occurred_at ? new Date(item.occurred_at).toLocaleString() : "--";
    const title = item.title || item.message || "诊断事件";
    li.textContent = `${time} ${title}`;
    list.appendChild(li);
  });
}

function renderAlertStatus(data) {
  const payload = data || {};
  const alerts = payload.alerts || {};
  const telegram = payload.telegram || {};
  const email = payload.email || {};
  const state = payload.state || {};

  const enabled = Boolean(alerts.enabled);
  setText("alerts-enabled", enabled ? "已开启" : "未开启");
  setText("alerts-message", enabled ? "告警已开启，出现触发条件时将发送通知。" : "告警已关闭，不会发送通知。");
  setText("alerts-config-state", enabled ? "已开启" : "未开启");
  setText("alerts-min-severity", alerts.min_severity || "--");
  setText("alerts-cooldown", `${alerts.cooldown_seconds ?? "--"}s`);
  setText("alerts-recovery", String(alerts.send_recovery ?? "--"));
  setText("alerts-telegram", telegram.enabled ? (telegram.ready ? "已开启且就绪" : "已开启但配置不完整") : "未开启");
  setText("alerts-email", email.enabled ? (email.ready ? "已开启且就绪" : "已开启但配置不完整") : "未开启");
  setText("alerts-active", state.active_alert_count ?? "--");
  setText("alerts-last-sent", state.last_sent_at ? new Date(state.last_sent_at).toLocaleString() : "--");
  setText("alerts-safe-to-test", payload.safe_to_test ? "可发送测试通知" : "不可发送测试通知");
}

function renderAlertConfigCheck(data) {
  const payload = data || {};
  const telegram = payload.channels?.telegram || {};
  const email = payload.channels?.email || {};
  const configMessage = el("alerts-config-message");
  if (configMessage) {
    configMessage.textContent = payload.message || "告警配置读取失败";
  }
  setText("alerts-config-state", payload.status === "healthy" ? "可用" : "未就绪");
  setText("alerts-safe-to-test", payload.safe_to_test ? "可发送测试通知" : "不可发送测试通知");
  setText("alerts-telegram", telegram.enabled ? (telegram.ready ? "已开启且就绪" : "已开启但配置不完整") : "未开启");
  setText("alerts-email", email.enabled ? (email.ready ? "已开启且就绪" : "已开启但配置不完整") : "未开启");
}

function renderMeta(meta) {
  const payload = meta || {};
  const host = payload.configured_host || "127.0.0.1";
  const port = payload.configured_port || 3001;
  const publicEntry = String(payload.public_entry || "tower.conanxin.com").replace(/^https?:\/\//, "");
  const accessProtection = payload.access_protection || "Cloudflare Access";
  const accessMode = payload.external_access_mode || "Cloudflare Access + Tunnel";

  setText(
    "runtime-bar",
    `运行模式：本地只读 · 绑定地址：${host}:${port} · 外部入口：${publicEntry} · 访问保护：${accessProtection} · 公网直连：${payload.direct_public_bind ? "有" : "无"}`,
  );
  setText("runtime-public-entry", publicEntry);
  setText("runtime-access-protection", accessProtection);
  setText("runtime-management-entry", resolveManagementDisplayUrl(currentManagement?.panel_public_url, currentManagement?.panel_public_display_url) || managementPanelMissingText);
  setText("runtime-mode", "本地只读");
  setText("runtime-endpoint", `${host}:${port}`);
  setText("runtime-public-bind", payload.direct_public_bind ? "有" : "无");
}

const defaultMeta = {
  configured_host: "127.0.0.1",
  configured_port: 3001,
  public_entry: "tower.conanxin.com",
  direct_public_bind: false,
  external_access_mode: "Cloudflare Access + Tunnel",
  access_protection: "Cloudflare Access",
};

let currentManagement = {};

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
      readable_summary: `健康巡检失败：${error.message}`,
      checks: [],
      risk_summary: [],
      checked_at: new Date().toISOString(),
    });
  }
}

async function refreshManagement() {
  try {
    const response = await fetch("/api/management", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    currentManagement = await response.json();
    renderManagement(currentManagement);
  } catch (error) {
    currentManagement = {
      enabled: false,
      status: "unknown",
      message: `管理入口检查失败：${error.message}`,
      panel_local_url: "",
      panel_public_url: "",
      panel_public_display_url: "",
      detected_scheme: "unknown",
      recommended_local_url: "",
      protocol_warning: false,
      tcp_reachable: false,
      open_in_new_tab: true,
      access_note: "建议通过 Cloudflare Access + 3X-UI 登录双层保护访问。",
      readonly_note: "Control Tower 只负责健康监测和管理入口，不读取或修改 3X-UI 配置。",
      show_local_target: true,
    };
    renderManagement(currentManagement);
  }
}

async function refreshAlerts() {
  try {
    const response = await fetch("/api/alerts/status", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderAlertStatus(await response.json());
  } catch {
    setText("alerts-message", "告警状态暂不可用。");
  }
}

async function refreshAlertConfigCheck() {
  try {
    const response = await fetch("/api/alerts/config-check", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderAlertConfigCheck(await response.json());
  } catch {
    setText("alerts-config-message", "告警配置校验暂不可用。");
  }
}

async function refreshDiagnostics() {
  try {
    const response = await fetch("/api/diagnostics", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderDiagnostics(await response.json());
  } catch {
    renderDiagnostics({ items: [] });
  }
}

async function refreshHistory() {
  try {
    const [summaryResp, eventsResp] = await Promise.all([
      fetch("/api/history/summary", { cache: "no-store" }),
      fetch("/api/events?limit=5", { cache: "no-store" }),
    ]);
    const summary = summaryResp.ok ? await summaryResp.json() : { enabled: false };
    const events = eventsResp.ok ? await eventsResp.json() : { enabled: false, items: [] };
    renderHistory(summary, events.items || []);
  } catch {
    renderHistory({ enabled: false }, []);
  }
}

async function refreshMeta() {
  try {
    const response = await fetch("/api/meta", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    renderMeta(await response.json());
  } catch {
    renderMeta(defaultMeta);
  }
}

async function sendTestAlert() {
  const output = el("test-alert-result");
  if (output) {
    output.textContent = "正在发送测试告警…";
  }
  try {
    const response = await fetch("/api/alerts/test", { method: "POST" });
    const data = await response.json();
    if (output) {
      if (data.sent) {
        output.textContent = "测试告警已触发。";
      } else if (typeof data.message === "string") {
        output.textContent = `测试告警结果：${data.message}`;
      } else {
        output.textContent = "测试告警已跳过。";
      }
    }
    await refreshAlerts();
    await refreshAlertConfigCheck();
  } catch (error) {
    if (output) {
      output.textContent = `测试告警失败：${error.message}`;
    }
  }
}

function bindNavigationGuards() {
  const managementButton = el("management-open-button");
  if (managementButton) {
    managementButton.addEventListener("click", (event) => {
      const disabled = managementButton.getAttribute("aria-disabled") === "true";
      const targetUrl = managementButton.getAttribute("data-target-url");
      if (disabled || !targetUrl) {
        event.preventDefault();
        setText("management-disabled-note", managementDisabledHint);
        return;
      }

      const opened = window.open(targetUrl, "_blank", "noopener,noreferrer");
      if (!opened) {
        const fallback = document.createElement("a");
        fallback.href = targetUrl;
        fallback.target = "_blank";
        fallback.rel = "noopener noreferrer";
        fallback.style.display = "none";
        document.body.appendChild(fallback);
        fallback.click();
        fallback.remove();
      }
    });
  }

  const testAlertButton = el("test-alert-button");
  if (testAlertButton) {
    testAlertButton.addEventListener("click", sendTestAlert);
  }
}

function renderManagementReadOnlyHint() {
  const maskNote = el("management-readonly-note");
  if (!maskNote) {
    return;
  }
  maskNote.textContent = "Control Tower 只负责健康监测和管理入口，不读取或修改 3X-UI 配置。";
}

function renderExternalAccessInfo() {
  const entry = el("runtime-management-entry");
  if (entry) {
    entry.title = "为避免泄露管理入口隐藏路径，界面仅显示脱敏入口。";
  }
}

async function refreshAll() {
  await Promise.all([
    refreshMeta(),
    refreshHealth(),
    refreshManagement(),
    refreshAlerts(),
    refreshAlertConfigCheck(),
    refreshDiagnostics(),
    refreshHistory(),
  ]);
  renderManagementReadOnlyHint();
  renderExternalAccessInfo();
}

refreshAll();
bindNavigationGuards();
window.setInterval(refreshMeta, 30000);
window.setInterval(refreshHealth, 30000);
window.setInterval(refreshManagement, 60000);
window.setInterval(refreshAlerts, 30000);
window.setInterval(refreshAlertConfigCheck, 60000);
window.setInterval(refreshDiagnostics, 30000);
window.setInterval(refreshHistory, 60000);
