# Phase 1E Local-Only Hardening and VPS Validation Report

## 本阶段目标

对 Conan VPS Control Tower 进行真实 VPS 上线前的 local-only 硬化与验证准备，确认 Dashboard、API、告警、诊断模块可以安全运行且不影响现有代理工具。

## 新增 / 修改文件

新增：

- `scripts/preflight-local-only.sh`
- `scripts/collect-redacted-vps-status.sh`
- `docs/SYSTEMD_LOCAL_ONLY.md`
- `docs/REAL_VPS_VALIDATION_CHECKLIST.md`
- `docs/DASHBOARD_SMOKE_TEST.md`
- `tests/test_local_only_config.py`
- `tests/test_docs_safety.py`
- `reports/PHASE_1E_LOCAL_ONLY_HARDENING_AND_VPS_VALIDATION_REPORT.md`

修改：

- `.gitignore`
- `README.md`
- `CHANGELOG.md`
- `docs/ROADMAP.md`
- `docs/DEPLOYMENT.md`
- `docs/LIVE_VPS_DEPLOYMENT_VERIFICATION.md`
- `docs/SSH_TUNNEL_ACCESS.md`
- `docs/REAL_VPS_CONFIG_GUIDE.md`
- `docs/ALERTING.md`
- `docs/DIAGNOSTICS.md`

## 实现内容

- 新增部署前 local-only preflight 脚本。
- 新增真实 VPS 脱敏状态采集脚本。
- 新增 systemd local-only 文档、真实 VPS 验证清单、Dashboard smoke test 文档。
- 增加 local-only 配置和文档安全测试。
- 收紧 Deployment 文档中关于 `0.0.0.0` 的表述。

## local-only hardening review 结果

- app 默认 host：`127.0.0.1`。
- config.example.yaml 默认 `server.host`：`127.0.0.1`。
- systemd service 默认：`--host 127.0.0.1 --port 3001`。
- scripts/run-dev.sh 默认：`--host 127.0.0.1 --port 3001`。
- README 明确 local-only。
- ALERTING / DIAGNOSTICS / DEPLOYMENT 文档说明不需要公网暴露。

## 对现有代理工具的影响分析

- 是否修改 3X-UI：否。
- 是否重启代理：否。
- 是否改防火墙：否。
- 是否开放公网端口：否。
- 是否占用代理端口：否。
- 是否自动执行诊断命令：否。

## 是否执行真实 VPS 验证

未执行。

原因：当前环境未提供 `CONTROL_TOWER_VPS_HOST` / `CONTROL_TOWER_VPS_USER`，因此没有尝试 SSH。

## 用户手动执行步骤

```bash
mkdir -p ~/apps
cd ~/apps
git clone https://github.com/conanxin/conan-vps-control-tower.git
cd conan-vps-control-tower
git checkout main
bash scripts/deploy-local-only.sh
bash scripts/preflight-local-only.sh
```

启动后可执行：

```bash
bash scripts/check-local-only-status.sh
bash scripts/collect-redacted-vps-status.sh
```

## 测试结果

`python -m pytest` 已通过：

```text
45 passed
```

Shell 脚本语法检查已通过：

```text
bash -n scripts/preflight-local-only.sh
bash -n scripts/collect-redacted-vps-status.sh
bash -n scripts/deploy-local-only.sh
bash -n scripts/check-local-only-status.sh
```

## 当前系统状态

项目仍保持只读、local-only、低配 VPS 友好。真实 VPS 验证等待用户手动执行。

## 下一阶段建议

首选 Phase 1E.1：v0.2.0-alpha release preparation，如果真实 VPS 验证通过。

备选 Phase 2：Project Control Tower foundation，如果暂不发布。
