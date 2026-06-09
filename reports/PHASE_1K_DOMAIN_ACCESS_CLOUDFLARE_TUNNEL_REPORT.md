# Phase 1K Domain Access via Cloudflare Tunnel Report

## 1. 本阶段目标

- 为手机浏览器和域名访问设计安全路径。
- 为 Conan VPS Control Tower 与 3X-UI 面板分别提供 Cloudflare Tunnel 映射模板。
- 保持本项目只读、local-only，不修改代理栈，不开放裸奔公网端口。

## 2. 为什么选择 Cloudflare Tunnel

- 不需要 VPS 监听公网 `80/443`。
- 不需要把 Conan VPS Control Tower 改成 `0.0.0.0`。
- 可以把本地服务保持在 `127.0.0.1`。
- 可以使用 Cloudflare Access 做邮箱级访问控制，适合手机浏览器访问。

## 3. 为什么暂不选择 Caddy/Nginx

- Caddy/Nginx 通常需要占用或接管 `80/443`。
- 代理节点的 `80/443` 可能已被现有代理服务使用。
- 本阶段目标是最小风险的访问设计，不做反向代理接管。

## 4. 新增 / 修改文件

- 新增：
  - `docs/DOMAIN_ACCESS_CLOUDFLARE_TUNNEL.md`
  - `docs/CLOUDFLARE_ACCESS_POLICY.md`
  - `deploy/cloudflare-tunnel/config.example.yml`
  - `scripts/discover-panel-and-tower-local.sh`
  - `scripts/check-domain-access-readiness.sh`
  - `reports/PHASE_1K_DOMAIN_ACCESS_CLOUDFLARE_TUNNEL_REPORT.md`
- 修改：
  - `README.md`
  - `docs/OPERATIONAL_RUNBOOK.md`
  - `docs/ROADMAP.md`
  - `CHANGELOG.md`

## 5. 对现有代理工具影响分析

- 是否修改 3X-UI：否
- 是否重启 3X-UI / xray / sing-box / v2ray / proxy core：否
- 是否修改防火墙：否
- 是否开放公网端口：否
- 是否绑定 `0.0.0.0`：否
- 是否占用 `80/443`：否
- 是否写入真实域名/token：否

## 6. 未执行的危险操作

- 未执行 `cloudflared tunnel create`
- 未执行 `cloudflared login`
- 未安装 `cloudflared`
- 未创建 Cloudflare DNS 记录
- 未修改 3X-UI 配置
- 未修改防火墙
- 未创建 release 或移动 tag

## 7. 后续真正绑定域名需要用户提供

- 域名，例如 `YOUR_DOMAIN`
- Cloudflare 账号权限
- 3X-UI 面板端口确认：`YOUR_3XUI_PANEL_PORT`
- 是否允许安装 `cloudflared`
- 是否允许创建 tunnel 与 Access policy

## 8. 测试结果

- 本地执行 `python -m pytest`：`101 passed`。
- 本地 PowerShell 环境未提供 `bash` 命令，因此未执行本地 `bash -n`。
- 新增测试覆盖文档、模板和脚本安全约束。

## 9. 下一阶段建议

Phase 1K-Live：Configure Cloudflare Tunnel with user-provided domain.
