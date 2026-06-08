# Phase 1B Domain / TLS / Traffic Risk Report

## 本阶段目标

在现有只读代理健康 Dashboard 基础上，增加域名解析风险、TLS 证书有效期风险、本地流量估算风险判断，让用户能看到代理常见外部依赖风险。

## 新增 / 修改文件

新增：

- `app/health/domain_checker.py`
- `app/health/tls_checker.py`
- `docs/DOMAIN_TLS_TRAFFIC_RISK.md`
- `data/.gitkeep`
- `tests/test_domain_checker.py`
- `tests/test_tls_checker.py`
- `tests/test_traffic_checker.py`
- `reports/PHASE_1B_DOMAIN_TLS_TRAFFIC_RISK_REPORT.md`

修改：

- `.gitignore`
- `config.example.yaml`
- `app/config.py`
- `app/models.py`
- `app/main.py`
- `app/health/evaluator.py`
- `app/health/traffic_checker.py`
- `app/static/index.html`
- `app/static/styles.css`
- `app/static/app.js`
- `tests/test_config.py`
- `tests/test_health_evaluator.py`
- `README.md`
- `CHANGELOG.md`
- `docs/HEALTH_MODEL.md`
- `docs/ROADMAP.md`
- `docs/REAL_VPS_CONFIG_GUIDE.md`

## 实现内容

- 增加可选 Domain / DNS checker，默认 disabled，不影响 overall。
- 增加可选 TLS certificate checker，默认 disabled，不保存证书全文。
- 将 Traffic checker 增强为基于 `/sys/class/net` 的本地接口 baseline 估算。
- 增加 `/api/domain`、`/api/tls`、`/api/traffic`。
- Dashboard 增加 Domain / DNS、TLS Certificate、Traffic Risk 展示。
- 增加 Phase 1B 文档和测试覆盖。

## 关键设计理由

- Domain/TLS 默认 disabled，避免未配置真实域名时产生误报。
- disabled optional checker 使用 `ignored: true`，保留 UI 可见性但不参与聚合。
- TLS 使用 Python 标准库 `ssl` 和 `socket`，不引入重型依赖。
- DNS 使用 Python 标准库 `socket.getaddrinfo`，不依赖 `dig` 或 `nslookup`。
- Traffic 使用本地接口计数和本地 state 文件，不接入 provider API，不读取账号信息。

## 对现有代理工具的影响分析

- 是否修改 3X-UI：否。
- 是否重启代理：否。
- 是否改防火墙：否。
- 是否开放公网端口：否。
- 是否占用代理端口：否。
- 是否绑定 `0.0.0.0`：否。
- 是否读取或提交代理 UUID、密码、订阅链接、面板密码、真实 IP、真实域名、token：否。

## 流量统计局限说明

流量统计是本地估算，基于 Linux `/sys/class/net/<interface>/statistics/rx_bytes` 和 `tx_bytes`。它可能与 VPS provider billing 不一致，原因包括 provider 计费口径、重启、接口变化、baseline 创建时间和流量方向差异。

## 测试结果

`python -m pytest` 已通过：

```text
17 passed
```

API smoke check 已通过：

```text
/api/health 200
/api/domain 200
/api/tls 200
/api/traffic 200
```

## 当前系统状态

项目仍保持轻量、只读、local-only。Phase 1B 已在代码中加入 Domain / TLS / Traffic 风险增强，默认不会启用 Domain/TLS 真实目标。

## 下一阶段建议

Phase 1C：Telegram / Email Alerting

- 增加可选 Telegram / Email 告警。
- 支持告警阈值与冷却时间。
- 默认关闭告警。
- 继续保持只读、不自动修复、不修改代理工具。
