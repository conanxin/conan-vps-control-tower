# Phase 1A.1 Open Source Alpha Release Report

## 本阶段目标

把 Phase 1A MVP 整理成可正式展示的 `v0.1.0-alpha` 开源项目，补齐 README 展示、开源协作文件、Issue 模板、最小 CI、发布说明、阶段报告和 GitHub Release 准备。

## 已修改 / 新增文件

修改：

- `README.md`

新增：

- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/workflows/ci.yml`
- `docs/release/RELEASE_NOTES_v0.1.0-alpha.md`
- `docs/media/README.md`
- `docs/media/dashboard-placeholder.md`
- `reports/PHASE_1A1_OPEN_SOURCE_ALPHA_RELEASE_REPORT.md`

## 设计理由

- README 从 MVP 状态升级为 alpha 展示页，明确项目阶段、默认本地运行模式、目标用户和安全边界。
- CHANGELOG 与 release notes 为第一个公开 tag 提供清晰上下文。
- CONTRIBUTING 与 SECURITY 保持简洁，强调轻量、只读、不提交敏感信息。
- GitHub Issue 模板把问题报告引导到非敏感复现、低配 VPS 适配和只读边界。
- CI 只运行 pytest，不加入安全扫描、复杂 matrix、发布自动化或容器编排，避免超过个人项目第一版需要。

## 对现有代理工具的影响分析

本阶段没有修改运行时 checker 行为，也没有新增任何会影响代理服务的代码路径。

- 不修改 3X-UI 配置。
- 不重启代理服务。
- 不修改防火墙。
- 不读取、不保存代理节点明文、UUID、密码、订阅链接或 token。
- 仍然默认绑定 `127.0.0.1:3001`。

## 测试结果

`python -m pytest` 已通过：

```text
6 passed
```

## Git commit hash

Phase 1A.1 主提交：

```text
99ff748
```

发布元信息补充提交和最终 tag 指向的提交以最终输出为准。

## tag 状态

`v0.1.0-alpha` annotated tag 已创建并推送到 GitHub。

## GitHub release 状态

GitHub prerelease 已创建成功：

```text
https://github.com/conanxin/conan-vps-control-tower/releases/tag/v0.1.0-alpha
```

## GitHub repo description / topics 是否设置成功

已通过 `gh repo edit` 设置成功：

- description: `A lightweight, read-only health dashboard for personal VPS proxy nodes.`
- topics: `vps`, `proxy`, `monitoring`, `fastapi`, `self-hosted`, `3x-ui`

## 当前系统状态

项目处于 `v0.1.0-alpha` 发布准备阶段，核心功能仍为 Phase 1A 只读健康 Dashboard MVP。

## 下一阶段建议

Phase 1A.2：Live VPS Deployment Verification

- 在真实 DMIT VPS 上以 `127.0.0.1:3001` 运行。
- 配置真实 3X-UI 面板端口、代理端口、进程名。
- 通过 SSH tunnel 查看 Dashboard。
- 记录真实 VPS 下的检测结果。
- 不开放公网访问。
