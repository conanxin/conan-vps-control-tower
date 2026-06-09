const statusClassList = ["healthy", "warning", "degraded", "critical", "unknown", "not-configured"];

const statusLabel = {
  healthy: "健康",
  warning: "警告",
  degraded: "降级",
  critical: "严重",
  unknown: "未知",
  "not-configured": "未配置",
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
  "TLS check failed or certificate is critical": "TLS 证书检查失败或已到达临界状态",
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
  "Not enough data to estimate risk.": "当前数据不足，暂无法评估风险。",
  "All configured health checks look healthy.": "已配置健康检查均正常。",
  "All configured health checks look healthy. Not configured: domain_dns, tls_certificate.": "已启用的健康检查均正常。域名 / DNS 与 TLS 证书检查尚未配置。",
  "All configured health checks look healthy. Not configured:": "已配置健康检查均正常，未配置：",
  "All monitored VPS and proxy health checks look healthy.": "已监控的 VPS 与代理健康检查均正常。",
  "Some checks could not determine a status. Review permissions, platform support, and configuration.": "部分检查无法判定状态，请确认权限、平台支持与配置。",
  "Health status is unknown because no checks were executed.": "本次未执行检查，健康状态暂不明。",
  "No visible risks from current checks.": "当前未发现可见风险。",
  "No active diagnostic issues detected.": "未发现需要处理的诊断问题。",
  "No active diagnostic issues detected": "未发现需要处理的诊断问题。",
  "No risk conditions detected from current checks.": "未发现当前活跃风险。",
  "No active risks": "当前没有活跃风险。",
  "History recovered": "历史恢复记录已更新。",
  "Could not load alert config": "告警配置检查失败。",
};

const moduleLabels = {
  vps_system: "VPS 状态",
  proxy_core: "代理核心",
  xui_panel: "管理面板",
  proxy_ports: "端口",
  domain_dns: "域名 / DNS",
  tls_certificate: "TLS 证书",
  traffic: "流量风险",
};

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

function setCardState(card, status, isIgnored) {
  card.classList.remove(...statusClassList);
  if (isIgnored) {
    card.classList.add("not-configured");
    return;
  }
  card.classList.add(normalizeStatus(status));
}

function updateCard(check) {
  const card = document.querySelector(`[data-check="${check.name}"]`);
  if (!card) {
    return;
  }
  const ignored = Boolean(check.ignored);
  const status = normalizeStatus(check.status);

  setCardState(card, status, ignored);
  const message = translateMessage(check.message);
  card.querySelector("h3").textContent = toDisplayStatus(ignored ? "not-configured" : status);
  card.querySelector(".message").textContent = message;
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
    const resolvedCount = Array.isArray(resolved) ? resolved.length : Object.values(resolved).reduce((count, ips) => {
      if (Array.isArray(ips)) {
        return count + ips.length;
      }
      return count;
    }, 0);
    const hasExpected = Array.isArray(details.expected_ips) && details.expected_ips.length > 0;
    const hasMismatch = Array.isArray(details.mismatches) && details.mismatches.length > 0;

    setDetail(card, "resolved_ip_count", check.ignored ? "未配置" : String(resolvedCount));
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
    setDetail(card, "days_remaining", check.ignored ? "未配置" : formatInt(target.days_remaining, "--"));
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

function getPipelineState(check) {
  if (!check) {
    return "unknown";
  }
  if (check.ignored) {
    return "ok";
  }
  if (["warning", "degraded", "critical"].includes(normalizeStatus(check.status))) {
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
      node.classList.add("unknown");
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
        li.textContent = `${label}：${translateMessage(check.message)}`;
        riskSummary.appendChild(li);
      });
    }
  }

  const optionalChecks = document.getElementById("optional-checks");
  if (optionalChecks) {
    optionalChecks.setAttribute("aria-label", "未配置的可选检查");
    optionalChecks.replaceChildren();
    ["domain_dns", "tls_certificate"].forEach((name) => {
      const check = checks.find((item) => item.name === name);
      const label = moduleLabels[name] || name;
      const li = document.createElement("li");
      if (!check || check.ignored) {
        li.textContent = `${label}：未配置`;
      } else {
        li.textContent = `${label}：已启用`;
      }
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
    const host = parsed.hostname || "";
    if (!host) {
      return url;
    }
    const hasHidden =
      Boolean(parsed.pathname && parsed.pathname !== "/") ||
      Boolean(parsed.search || parsed.hash);
    return hasHidden ? `${host} / 已配置隐藏路径` : host;
  } catch {
    return url;
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

function parseHost(url) {
  if (!url) {
    return "";
  }
  try {
    return new URL(url).hostname || "";
  } catch {
    return "";
  }
}

function maskPanelPathHint(url) {
  const host = parseHost(url);
  if (!host) {
    return "--";
  }
  try {
    const parsed = new URL(url);
    const hasHidden =
      Boolean(parsed.pathname && parsed.pathname !== "/") ||
      Boolean(parsed.search || parsed.hash);
    return hasHidden ? `${host} / 已配置隐藏路径` : host;
  } catch {
    return host;
  }
}

function renderMaskedPanelEntry(url) {
  const host = maskPanelPathHint(url);
  if (!host || host === "--") {
    return "--";
  }
  return host.includes("/已配置隐藏路径") ? host : `${host} / 已配置隐藏路径`;
}

function renderManagement(data) {
  const status = data.enabled === false ? "not-configured" : normalizeStatus(data.status);
  const button = document.getElementById("management-open-button");
  const publicUrl = data.panel_public_url || "";
  const publicDisplay = data.panel_public_display_url || parsePublicDisplay(publicUrl);

  const accessNote =
    data.access_note || "建议通过 Cloudflare Access 与双重校验进行保护后访问管理入口。";
  const readOnlyNote =
    data.readonly_note || "Control Tower 不读取或修改 3X-UI 配置。";

  document.getElementById("management-status").textContent = toDisplayStatus(status);
  document.getElementById("management-message").textContent = data.message || "未检测到管理入口信息。";
  document.getElementById("management-status").closest(".card").classList.remove(...statusClassList);
  document.getElementById("management-status").closest(".card").classList.add(status);

  const localEndpoint = data.recommended_local_url || data.panel_local_url || "";
  document.getElementById("management-local-entry").textContent =
    data.show_local_target !== false
      ? parseManagementEndpoint(localEndpoint || data.panel_local_url)
      : "暂未开启显示本地入口";
  const recommendedUrl = data.recommended_local_url || data.panel_local_url || "";
  document.getElementById("management-recommended-url").textContent =
    data.show_local_target !== false && recommendedUrl
      ? parseManagementEndpoint(recommendedUrl)
      : "暂未开启显示本地入口";

  const publicDisplayText =
    publicDisplay && publicDisplay.includes("/已配置隐藏路径")
      ? renderMaskedPanelEntry(publicDisplay)
      : renderMaskedPanelEntry(publicUrl);
  document.getElementById("management-public-entry").textContent = publicDisplayText || "--";

  const protocolWarningEl = document.getElementById("management-protocol-warning");
  if (protocolWarningEl) {
    protocolWarningEl.hidden = !Boolean(data.protocol_warning);
    protocolWarningEl.textContent = data.protocol_warning
      ? `检测到面板入口协议可能不匹配。建议使用 ${data.recommended_local_url || "https://127.0.0.1:2053"} 作为 Tunnel target。`
      : "";
  }

  document.getElementById("management-access-note").textContent =
    accessNote || "建议通过 Cloudflare Access 与双重校验进行保护后访问管理入口。";
  document.getElementById("management-readonly-note").textContent = readOnlyNote;

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
    button.target = "_self";
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
  document.getElementById("readable-summary").textContent =
    translateMessage(data.readable_summary) || "健康状态读取中。";
  document.getElementById("last-checked").textContent = `最后检查：${data.checked_at ? new Date(data.checked_at).toLocaleString() : "--"}`;

  checks.forEach(updateCard);
  renderPipeline(checks);
  renderRiskAndOptional(checks);
}

function renderDiagnostics(data) {
  const summary = document.getElementById("diagnostics-summary");
  const item = Array.isArray(data.items) ? data.items[0] : null;

  if (!item) {
    summary.textContent = "未发现需要处理的诊断问题。";
    document.querySelector("#top-diagnosis h3").textContent = "当前无优先诊断";
    document.getElementById("diagnosis-impact").textContent = "当前系统状态较稳。";
    document.getElementById("diagnosis-first-check").textContent = "如有异常，优先确认代理核心与端口状态。";
    document.getElementById("diagnosis-related").textContent = "相关模块：-";
    document.getElementById("diagnosis-confidence").textContent = "置信度：高";
    document.getElementById("diagnosis-commands").textContent = "当前无需执行命令。";
    return;
  }

  const panelPort = getPanelPort(currentManagement?.panel_local_url || currentManagement?.panel_public_url);
  const host = parseHost(currentManagement?.panel_local_url || currentManagement?.panel_public_url) || "127.0.0.1";
  const panelAddress = currentManagement?.panel_local_url || currentManagement?.panel_public_url || "";
  const panelPortText = panelPort || "（请先确认面板端口）";
  const domainHost = parseHost(panelAddress) || "panel.conanxin.com";
  const commands = Array.isArray(item.read_only_commands) ? item.read_only_commands : [];
  const commandsText = commands
    .map((command) =>
      String(command)
        .replace(/YOUR_PROXY_PORT/g, panelPortText)
        .replace(/YOUR_PANEL_PORT/g, panelPortText)
        .replace(/YOUR_PANEL_HOST/g, host)
        .replace(/YOUR_DOMAIN/g, domainHost)
        .replace("https://127.0.0.1", host ? `https://${host}` : "https://127.0.0.1"),
    )
    .join("\n");

  const title = `${item.title || "诊断提示"}（${toDisplayStatus(item.status || "unknown")}）`;
  const impact = item.impact || "请按优先级排查。";
  const firstCheck = item.suggested_first_check || "请检查相关模块状态。";
  const relatedModules = (item.related_modules || []).join("、") || "-";
  const confidence = item.confidence || "中";

  summary.textContent = `${data.summary || "诊断摘要："} ${item.title || ""}`;
  document.querySelector("#top-diagnosis h3").textContent = title;
  document.getElementById("diagnosis-impact").textContent = `影响：${impact}`;
  document.getElementById("diagnosis-first-check").textContent = `建议第一检查：${firstCheck}`;
  document.getElementById("diagnosis-related").textContent = `相关模块：${relatedModules}`;
  document.getElementById("diagnosis-confidence").textContent = `置信度：${confidence}`;

  const commandTextWithMask = `${readOnlyDiagnosticsNotice}\n${commandsText || "未提供只读诊断命令。"}`;
  document.getElementById("diagnosis-commands").textContent = commandTextWithMask;

  if (item.related_modules && item.related_modules.includes("xui_panel")) {
    document.getElementById("diagnosis-health-note").textContent = "面板异常不一定影响代理转发，当前代理核心与端口仍正常时可先不重启代理。"
  }
}

function renderHistory(summary, events) {
  const statusEl = document.getElementById("history-status");
  const windowStatusEl = document.getElementById("history-window-status");
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
    summaryEl.textContent = "健康历史功能未开启。";
    if (windowStatusEl) {
      windowStatusEl.textContent = "最近 24 小时：未开启";
    }
    [currentEl, worstEl, ratioEl, snapshotCountEl, eventCountEl, lastProblemEl, lastRecoveryEl].forEach((el) => {
      if (el) el.textContent = "--";
    });
    if (listEl) {
      listEl.replaceChildren(createNoDataLi("暂无历史事件。"));
    }
    return;
  }

  const currentStatus = summary.current_health_status || summary.latest_status || "--";
  const warningCount = Number(summary.warning_count || 0) + Number(summary.degraded_count || 0) + Number(summary.critical_count || 0);
  const warningLabel = warningCount > 0 ? `曾出现 ${warningCount} 次告警` : "无告警";
  const recoveredLabel = currentStatus === "healthy" && warningCount > 0 ? "，当前已恢复。" : "。";

  if (statusEl) {
    statusEl.textContent = `当前状态：${toDisplayStatus(currentStatus === "--" ? summary.status || "unknown" : currentStatus)}`;
  }
  if (windowStatusEl) {
    windowStatusEl.textContent = `最近 24 小时：${warningLabel}${recoveredLabel}`;
  }
  currentEl.textContent = currentStatus === "--" ? toDisplayStatus(summary.status || "unknown") : toDisplayStatus(currentStatus);
  worstEl.textContent = toDisplayStatus(summary.worst_status || "unknown");
  ratioEl.textContent = typeof summary.healthy_ratio === "number" ? `${summary.healthy_ratio.toFixed(1)}%` : "--";
  snapshotCountEl.textContent = `${summary.snapshot_count || 0}`;
  eventCountEl.textContent = `${summary.event_count || 0}`;
  lastProblemEl.textContent = summary.last_problem_at || "--";
  lastRecoveryEl.textContent = summary.last_recovery_at || "--";

  const currentText =
    toDisplayStatus(currentStatus === "--" ? summary.status || "unknown" : currentStatus) === "健康"
      ? `当前状态健康，24 小时内${warningLabel}，并已恢复。`
      : `当前状态${toDisplayStatus(currentStatus)}，24 小时内${warningLabel}。`;
  summaryEl.textContent = currentText;

  const visibleEvents = Array.isArray(events) ? events.slice(-5) : [];
  listEl.replaceChildren();
  if (visibleEvents.length === 0) {
    listEl.appendChild(createNoDataLi("暂无历史事件。"));
    return;
  }

  visibleEvents.forEach((item) => {
    const li = document.createElement("li");
    const time = item.occurred_at ? new Date(item.occurred_at).toLocaleString() : "--";
    const title = item.title || item.message || "诊断事件";
    li.textContent = `${time} ${title}`;
    listEl.appendChild(li);
  });
}

function createNoDataLi(text) {
  const li = document.createElement("li");
  li.textContent = text;
  return li;
}

function renderMeta(meta) {
  const host = meta.configured_host || "127.0.0.1";
  const port = meta.configured_port || 3001;

  const externalEntry =
    meta.public_entry || "tower.conanxin.com";
  const publicEntryDisplay = externalEntry.replace(/^https?:\/\//, "");
  const accessMode = meta.external_access_mode || "Cloudflare Access / Tunnel";
  const accessProtection = meta.access_protection || "Cloudflare Access / Tunnel";

  document.getElementById("runtime-bar").textContent =
    `本地只读 · 绑定：${host}:${port} · 外部入口：${publicEntryDisplay} · 访问态：${accessProtection} · 公网直连：${meta.direct_public_bind ? "有" : "无"}`;

  document.getElementById("runtime-mode").textContent = "本地只读";
  document.getElementById("runtime-endpoint").textContent = `${host}:${port}`;
  document.getElementById("runtime-public-entry").textContent = publicEntryDisplay;
  document.getElementById("runtime-access-protection").textContent = accessProtection;
  document.getElementById("runtime-public-bind").textContent = meta.direct_public_bind ? "有" : "无";

  const towerEntryEl = document.getElementById("external-tower-entry");
  const panelEntryEl = document.getElementById("external-panel-entry");
  if (towerEntryEl) {
    towerEntryEl.textContent = publicEntryDisplay;
  }
  if (panelEntryEl) {
    panelEntryEl.textContent =
      currentManagement && currentManagement.panel_public_display_url
      ? renderMaskedPanelEntry(currentManagement.panel_public_display_url)
      : "panel.conanxin.com / 已配置隐藏路径";
  }

  const tunnelNotes = document.querySelectorAll(".external-grid div");
  if (tunnelNotes.length >= 4) {
    tunnelNotes[3].querySelector("span").textContent = "访问态";
    tunnelNotes[3].querySelector("strong").textContent = accessMode.includes("Tunnel") ? accessMode : "Cloudflare Access / Tunnel";
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
    ? "告警已开启，出现触发条件时将发送通知。"
    : "告警已关闭，不会发送通知。";
  document.getElementById("alerts-config-state").textContent = alertsEnabled ? "已开启" : "已关闭";
  document.getElementById("alerts-min-severity").textContent = alerts.min_severity || "--";
  document.getElementById("alerts-cooldown").textContent = `${alerts.cooldown_seconds ?? "--"}s`;
  document.getElementById("alerts-recovery").textContent = String(alerts.send_recovery ?? "--");
  document.getElementById("alerts-telegram").textContent = telegram.enabled
    ? telegram.ready
      ? "已开启且就绪"
      : "已开启但配置不完整"
    : "未开启";
  document.getElementById("alerts-email").textContent = email.enabled
    ? email.ready
      ? "已开启且就绪"
      : "已开启但配置不完整"
    : "未开启";
  document.getElementById("alerts-active").textContent = state.active_alert_count ?? "--";
  document.getElementById("alerts-last-sent").textContent = state.last_sent_at
    ? new Date(state.last_sent_at).toLocaleString()
    : "--";

  const result = document.getElementById("alerts-safe-to-test");
  if (result) {
    result.textContent = data.safe_to_test ? "可发送测试通知" : "不可发送测试通知";
  }
}

function renderAlertConfigCheck(data) {
  const configMessageEl = document.getElementById("alerts-config-message");
  const telegram = data.channels?.telegram || {};
  const email = data.channels?.email || {};

  configMessageEl.textContent = data.message || "告警配置读取失败";
  document.getElementById("alerts-config-state").textContent = data.status === "healthy" ? "可用" : "未就绪";
  document.getElementById("alerts-safe-to-test").textContent = data.safe_to_test ? "可发送测试通知" : "不可发送测试通知";
  document.getElementById("alerts-telegram").textContent = telegram.enabled
    ? telegram.ready
      ? "已开启且就绪"
      : "已开启但配置不完整"
    : "未开启";
  document.getElementById("alerts-email").textContent = email.enabled
    ? email.ready
      ? "已开启且就绪"
      : "已开启但配置不完整"
    : "未开启";
}

function renderManagementReadOnlyHint() {
  const maskNote = document.getElementById("management-readonly-note");
  if (!maskNote) {
    return;
  }
  maskNote.textContent = "Control Tower 不读取或修改 3X-UI 配置。";
}

const readOnlyDiagnosticsNotice = "以下命令仅用于只读排查，不会自动执行。";
const readOnlyManagementHint = "如需修改代理配置，可通过“管理入口”进入 3X-UI 面板。";

let currentManagement = {};

async function refreshHealth() {
  try {
    const response = await fetch("/api/health", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    renderHealth(data);
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
    const data = await response.json();
    currentManagement = data;
    renderManagement(data);
  } catch (error) {
    currentManagement = {
      enabled: false,
      status: "unknown",
      message: `管理入口检查失败：${error.message}`,
      panel_local_url: "",
      panel_public_url: "",
      panel_public_display_url: "--",
      detected_scheme: "unknown",
      recommended_local_url: "",
      protocol_warning: false,
      tcp_reachable: false,
      open_in_new_tab: true,
      access_note: "建议通过 Cloudflare Access 与双重校验进行保护后访问管理入口。",
      readonly_note: "Control Tower 不读取或修改 3X-UI 配置。",
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
    document.getElementById("alerts-message").textContent = "告警状态暂不可用。";
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
    document.getElementById("alerts-config-message").textContent = "告警配置校验暂不可用。";
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
  const fallback = {
      configured_host: "127.0.0.1",
      configured_port: 3001,
      public_entry: "tower.conanxin.com",
      external_access_mode: "Cloudflare Access / Tunnel",
      direct_public_bind: false,
      access_protection: "Cloudflare Access / Tunnel",
    };
    renderMeta(fallback);
  }
}

async function sendTestAlert() {
  const output = document.getElementById("test-alert-result");
  output.textContent = "正在发送测试告警…";
  try {
    const response = await fetch("/api/alerts/test", { method: "POST" });
    const data = await response.json();
    if (data.sent) {
      output.textContent = "测试告警已触发。";
    } else if (typeof data.message === "string") {
      output.textContent = `测试告警结果：${data.message}`;
    } else {
      output.textContent = "测试告警已跳过。";
    }
    await refreshAlerts();
    await refreshAlertConfigCheck();
  } catch (error) {
    output.textContent = `测试告警失败：${error.message}`;
  }
}

function renderExternalAccessInfo() {
  const panelEl = document.getElementById("external-panel-entry");
  if (panelEl) {
    panelEl.title = "为避免泄露管理入口隐藏路径，界面仅显示脱敏入口。";
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

document.getElementById("test-alert-button").addEventListener("button", sendTestAlert);
const btn = document.getElementById("test-alert-button");
if (btn) {
  btn.addEventListener("click", sendTestAlert);
}

refreshAll();
window.setInterval(refreshMeta, 30000);
window.setInterval(refreshHealth, 30000);
window.setInterval(refreshManagement, 60000);
window.setInterval(refreshAlerts, 30000);
window.setInterval(refreshAlertConfigCheck, 60000);
window.setInterval(refreshDiagnostics, 30000);
window.setInterval(refreshHistory, 60000);
