# Phase 1L.4 Dashboard Domain Access UX Polish Report

## 本阶段目标

在 `tower.conanxin.com` 和 `panel.conanxin.com` 已经通过 Cloudflare Access + Tunnel 跑通后，将 Dashboard 从本地调试体验打磨为正式中文控制台体验。

## 当前域名访问状态

- Control Tower 外部入口：`tower.conanxin.com`
- 3X-UI 管理入口：`panel.conanxin.com / 已配置隐藏路径`
- 访问保护：Cloudflare Access
- 本项目服务绑定：`127.0.0.1:3001`
- 公网直连：无

## UI 问题

- 顶部仍偏向 SSH Tunnel 语境。
- 部分状态说明仍为英文。
- 管理入口卡片在长 URL 和隐藏路径场景下拥挤。
- 隐藏路径展示需要继续脱敏，避免泄露 3X-UI 入口。
- 健康历史中的历史异常容易和当前健康状态混淆。

## 修复内容

- 顶部状态栏改为展示本地只读、绑定地址、外部入口、Cloudflare Access 和公网直连状态。
- 管理入口卡片改为宽卡片视觉，展示脱敏公开入口、本地入口、推荐本地入口和保护方式。
- 管理入口按钮继续使用完整 `panel_public_url`，但界面只展示脱敏后的公开入口。
- 增加中文状态和诊断标题映射，减少 Dashboard 英文文案。
- 健康历史区分当前状态和最近 24 小时历史告警。
- 增加长 URL 防溢出样式。

## 中文乱码修复

- 管理入口说明改为前端固定中文 fallback。
- Dashboard 测试覆盖 `????`、历史乱码片段和隐藏路径明文。

## 管理入口重构

- 标题：`管理入口：3X-UI 面板`
- 公开入口展示：`panel.conanxin.com / 已配置隐藏路径`
- 标签：`公开入口已脱敏显示`
- 按钮：`进入 3X-UI 面板`
- 边界说明：Control Tower 只负责健康监测和管理入口，不读取或修改 3X-UI 配置。

## Cloudflare 访问状态文案

Dashboard 当前明确展示：

- 外部入口：`tower.conanxin.com`
- 访问保护：Cloudflare Access
- 公网直连：无

这表示服务自身仍未绑定公网地址，外部访问由 Cloudflare Tunnel 代理到本地回环地址。

## 对代理影响分析

- 是否修改 3X-UI：否
- 是否重启 3X-UI：否
- 是否重启代理核心：否
- 是否修改防火墙：否
- 是否开放公网端口：否
- 是否调用 3X-UI 写接口：否
- 是否输出隐藏路径：否

## 测试结果

本地执行 `python -m pytest`：

```text
128 passed, 4 warnings
```

## 远端验证结果

待提交并推送后执行远端验证。预期只重启 `conan-vps-control-tower.service`，不触碰 3X-UI、代理核心或防火墙。

## 下一阶段建议

Phase 1M：Cloudflare Access operational polish and masked screenshot capture。
