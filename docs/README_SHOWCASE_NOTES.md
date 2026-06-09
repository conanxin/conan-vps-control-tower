# README Showcase Notes

## README 展示策略

README 主要突出三条线：

1. 安全边界（local-only）
2. 能看懂的健康视图（总体状态、代理链路、活跃风险、诊断）
3. 快速上手（SSH tunnel + 30 秒刷新 + 常用命令）

文字上避免堆叠实现细节，先告诉用户“现在能知道什么、能在哪一步接着查”。

## 截图策略

- 默认先给占位文件，避免伪造或提交未脱敏截图。
- 有真实截图时，用脱敏后的本地-only 视图：
  - 标题与 local-only 状态条
  - 总体状态、代理链路、诊断摘要
  - 核心健康卡片
  - 活跃风险 + 未配置检查项
- 避免使用全屏带浏览器工具栏截图。

## 中文 Dashboard 定位

保持中文界面是为了减少个人运维用户的理解成本：

- 默认中文标签（整体更快识别）
- API 保持英文字段，兼容自动化与现有脚本

## 面向个人 VPS 用户的核心卖点

- local-only 本地只读边界清晰
- 重点问题不再“靠猜”，而是有层级化健康判断
- 诊断建议提供只读命令顺序，便于快速定位
- 告警默认关闭，风险通知可按需开启

## 面向开源访客的 30 秒理解路径

建议按以下顺序阅读：

1. Why local-only
2. What you can see
3. Screenshot/preview + demo walk through
4. Real VPS validation
5. 30 秒跑通命令清单（`tower-status.sh`）

## v0.2.1-alpha 预期补充说明

如果发布 `v0.2.1-alpha`，README 建议补充：

- 一张 `dashboard-zh-local-only-v0.2.png` 截图
- 运行时元信息（`/api/meta`）示例输出
- 新增安全检查（如新增模块）对应的“未配置 / 风险”展示说明
