# Phase 1L.3 Panel Health Check Repair Report

## 本阶段目标

修复 3X-UI 升级后 Control Tower 将 `xui_panel` 误判为 critical 的问题，并让诊断建议显示真实可执行的只读面板端口命令，而不是 `YOUR_PANEL_PORT` 占位符。

## 问题原因

- 远端 Control Tower 私有 `config.yaml` 的 `proxy.panel.url` 仍指向旧的本地面板入口。
- 3X-UI 升级后当前 `webPort` / `webBasePath` 与旧配置不一致。
- 旧健康检查没有对本地 HTTPS 自签证书做例外处理。
- 旧诊断规则使用静态 `YOUR_PANEL_PORT` 模板，无法根据健康检查详情生成真实端口命令。

## 远端配置修复

已只读读取 `/etc/x-ui/x-ui.db`，并只输出脱敏后的 `webBasePath` 摘要。

远端私有 `config.yaml` 仅更新 Conan VPS Control Tower 自身配置：

- `proxy.panel.url`: 指向当前确认的本地 HTTPS 面板入口，隐藏路径已脱敏记录。
- `management.panel_local_url`: 指向当前确认的本地 HTTPS 面板端口。
- `management.panel_public_url`: 保留公开入口与隐藏路径，仅存在于远端私有配置中。

未提交远端私有 `config.yaml`。

## 面板真实入口

报告中仅记录脱敏形式：

```text
https://127.0.0.1:YOUR_PANEL_PORT/<hidden>/
https://panel.conanxin.com/隐藏路径
```

## xui_panel 健康检查修复

- 本地 `https://127.0.0.1` / `localhost` / `::1` 面板检查允许跳过 TLS 证书校验。
- 非本地 HTTPS 不默认跳过证书校验。
- `200`, `301`, `302`, `307`, `401`, `403` 视为面板可达。
- `404` 视为路径可能不正确，不直接标记 healthy。
- API details 中隐藏路径显示为 `/<hidden>`。

## Diagnostics 占位符修复

- 面板诊断命令会优先使用 `xui_panel.details.port`。
- 有隐藏路径时使用 `/<hidden>`，不输出真实路径。
- 无法确认端口时显示“请先确认 3X-UI 面板端口。”
- 诊断说明补充：面板异常不一定影响代理转发；代理核心和端口正常时优先不要重启代理。

## 对现有代理影响分析

- 是否修改 3X-UI：否
- 是否重启 3X-UI：否
- 是否重启代理：否
- 是否改防火墙：否
- 是否开放公网端口：否
- 是否调用 3X-UI 写接口：否
- 是否读取或保存密码/cookie/token：否

## 测试结果

`python -m pytest`: 121 passed, 4 warnings.

## 远端验证结果

待远端更新与重启 `conan-vps-control-tower.service` 后补充。

## 下一阶段建议

Phase 1L.4: Cloudflare panel route alignment guide, if the user wants the public `panel.conanxin.com` route aligned with the current 3X-UI `webPort`.
