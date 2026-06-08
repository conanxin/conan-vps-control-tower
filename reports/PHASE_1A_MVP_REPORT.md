# Phase 1A MVP Report

## 本阶段目标

实现一个可以运行的本地只读 Proxy Health Dashboard MVP，用于查看 VPS、代理核心、3X-UI 面板、代理端口和基础流量状态。

## 实现内容

- `app/main.py`: FastAPI 应用入口，提供 `/`、`/api/health`、`/api/system`、`/api/proxy`。
- `app/config.py`: YAML 配置加载与默认值合并。
- `app/models.py`: checker 和聚合响应模型。
- `app/health/*`: 系统、进程、端口、HTTP、流量 checker 与健康聚合器。
- `app/static/*`: 原生 HTML/CSS/JS Dashboard，每 30 秒刷新。
- `scripts/*`: 开发启动、安装、卸载和 systemd service 模板。
- `tests/*`: evaluator、port checker、config loader 测试。

## 关键设计理由

- 所有 checker 捕获异常并返回 `unknown` 或明确失败状态，避免单点检测错误拖垮服务。
- evaluator 集中生成 `overall_status`、`readable_summary` 和 `risk_summary`，让 API 和 UI 保持简单。
- 端口默认检查 `127.0.0.1`，适合在 VPS 本机确认代理端口监听状态，不主动探测外部链路。
- UI 不依赖 CDN，不使用 React / Next，适合低配 VPS。
- systemd 默认绑定 `127.0.0.1:3001`，避免占用 80/443 或默认公网暴露。

## 对现有代理工具的影响分析

本阶段仅执行只读检测：

- 不修改 3X-UI 配置。
- 不重启代理服务。
- 不修改防火墙。
- 不读取、不保存节点明文、UUID、密码、订阅链接或 token。
- 不占用 80/443，仅使用 `127.0.0.1:3001`。

## 如何运行

```bash
./scripts/install.sh
./scripts/run-dev.sh
```

然后访问：

```text
http://127.0.0.1:3001
```

## 如何测试

```bash
pytest
```

## 当前限制

- 流量检查基于系统网卡自启动以来的累计计数，不是精确月度账单统计。
- systemd service 模板默认假设部署目录为 `/opt/conan-vps-control-tower`。
- 代理服务状态依赖 `systemctl`，非 systemd 环境会返回 `unknown`。
- 面板检测只判断 HTTP 可达性，不登录、不读取面板配置。

## 下一阶段建议

- Phase 1B 增加域名解析、TLS 证书、到期提醒和更准确的月度流量记录。
- 增加配置校验提示页面。
- 增加可选只读诊断命令展示。
