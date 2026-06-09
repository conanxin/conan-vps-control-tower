# Phase 1F.3 Report: README Screenshot and Demo Docs

## 本阶段目标

- 为 README 增加本地只读与 SSH Tunnel 导向的可展示内容。
- 补齐截图说明与占位规范。
- 补充 demo walkthrough 与展示说明文档。
- 更新展示相关文档与变更日志。

## 新增 / 修改文件

### 新增

- `docs/media/DASHBOARD_SCREENSHOT_GUIDE.md`
- `docs/media/dashboard-zh-local-only-v0.2.placeholder.md`
- `docs/DEMO_WALKTHROUGH.md`
- `docs/README_SHOWCASE_NOTES.md`
- `tests/test_readme_showcase_docs.py`
- `tests/test_media_docs.py`
- `reports/PHASE_1F3_README_SCREENSHOT_AND_DEMO_DOCS_REPORT.md`

### 修改

- `README.md`
- `docs/media/README.md`
- `docs/DASHBOARD_SMOKE_TEST.md`
- `docs/DASHBOARD_UX_POLISH.md`
- `docs/OPERATIONAL_RUNBOOK.md`
- `docs/ROADMAP.md`
- `CHANGELOG.md`

## README 展示改进内容

- 增加“界面预览”与“为什么是 local-only”板块。
- 补充“可见内容清单”与“实时验证摘要”。
- 强调默认中文 dashboard 与 SSH Tunnel 访问路径（`127.0.0.1:3001`）。
- 使用占位截图文件链接，避免未脱敏图片上墙。

## 截图安全策略

- 不提交真实截图文件，仅保留占位文件，等待脱敏后手动补充。
- 截图指引要求裁剪浏览器顶部、保持 127.0.0.1 本地地址显示。
- 禁止在截图中出现真实 IP、真实域名、token、UUID、订阅链接、面板密码。

## Demo walkthrough 内容

- 增加项目定位与非定位内容边界。
- 新增 Dashboard 解读路径：总体状态、代理链路、活跃风险、未配置项、诊断建议、告警状态。
- 列出常用排障命令清单，便于 README 一次性导航到操作。

## 对现有代理工具影响分析

- 是否修改 3X-UI：否
- 是否重启代理：否
- 是否改防火墙：否
- 是否开放公网端口：否
- 是否影响系统安全边界：无新增动作

## 测试结果

- 已添加并通过 `test_readme_showcase_docs.py` 与 `test_media_docs.py`。
- 保持既有核心测试通过（通过本次 `pytest` 全量运行）。

## 是否远端验证

- 本阶段为文档与展示素材更新，不需要新增远端服务验证。
- 已沿用阶段前的 real VPS 验证结果用于展示摘要。

## 当前系统状态

- Dashboard 默认中文界面已保持不变。
- `/api/meta` 与远端验证状态保留。
- 远端 service 仍为 local-only（`127.0.0.1:3001`，无公网监听）。

## 下一阶段建议

- Phase 2A：Project Registry foundation
