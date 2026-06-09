# Phase 1L.2 Management Entry URL Masking Report

## 1. 本阶段目标

- 修复管理入口卡片显示完整 3X-UI 隐藏路径的问题。
- 保持按钮继续使用完整 `panel_public_url`。
- UI 只展示脱敏后的 `panel_public_display_url`，避免长 URL 撑破卡片。

## 2. 解决的问题

- Dashboard 明文展示包含隐藏路径的 `panel_public_url`。
- 长 URL 会导致管理入口卡片横向溢出。
- 用户需要既能点击进入 3X-UI，又不在界面暴露隐藏路径。

## 3. 新增 / 修改文件

- 新增：
  - `reports/PHASE_1L2_MANAGEMENT_ENTRY_URL_MASKING_REPORT.md`
  - `tests/test_management_url_masking.py`
- 修改：
  - `app/management/models.py`
  - `app/management/panel.py`
  - `app/main.py`
  - `app/static/index.html`
  - `app/static/app.js`
  - `app/static/styles.css`
  - `README.md`
  - `CHANGELOG.md`
  - `docs/UNIFIED_MANAGEMENT_ENTRY.md`
  - `docs/CONTROL_TOWER_AND_3XUI_RELATIONSHIP.md`
  - `docs/DOMAIN_ACCESS_CLOUDFLARE_TUNNEL.md`
  - `docs/DASHBOARD_SMOKE_TEST.md`
  - `docs/OPERATIONAL_RUNBOOK.md`

## 4. 隐藏路径脱敏策略

- `panel_public_url` 保留完整 URL，用于按钮跳转。
- `panel_public_display_url` 用于 UI 展示。
- 无 path 时显示原始 origin，例如 `https://panel.conanxin.com`。
- 有 path/query/fragment 时显示 `https://panel.conanxin.com/隐藏路径`。
- 不在 Dashboard 明文展示真实隐藏路径。

## 5. UI 溢出修复

- 管理入口公开入口字段使用 `panel_public_display_url`。
- URL 单元格增加 `overflow-wrap: anywhere`、`word-break: break-word`。
- 管理入口卡片增加 overflow 约束，避免横向撑破布局。

## 6. 对现有代理工具影响分析

- 是否修改 3X-UI：否
- 是否重启 3X-UI / proxy core：否
- 是否修改防火墙：否
- 是否开放公网端口：否
- 是否绑定 `0.0.0.0`：否
- 是否调用 3X-UI 写 API：否
- 是否读取或保存 3X-UI 密码/cookie/token：否

## 7. 测试结果

- 本地执行 `python -m pytest`：`115 passed`。

## 8. 远端验证结果

- 计划远端 `git pull` 后只重启 `conan-vps-control-tower.service`。
- 验证 `/api/management` 同时返回完整 `panel_public_url` 和脱敏 `panel_public_display_url`。

## 9. 当前状态

- Control Tower 继续只做个人 VPS / 代理健康监测。
- 管理入口仅作为安全跳转入口，不合并 3X-UI、不调用 3X-UI 写接口。

## 10. 下一阶段建议

Phase 1L.3：Management entry screenshot and Cloudflare Access validation notes.
