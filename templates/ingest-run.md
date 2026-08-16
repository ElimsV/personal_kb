---
id: ingest-YYYYMMDD-short-slug
title: 本次入库运行标题
ingest_date: YYYY-MM-DD
recorded_at: YYYY-MM-DD
status: planned
trace_status: live
source_count: 0
candidate_count: 0
create_count: 0
reinforce_count: 0
update_count: 0
conflict_count: 0
ignore_count: 0
affected_knowledge_count: 0
weak_match_count: 0
single_source_create_count: 0
externally_verified_source_count: 0
validation_warning_count: 0
validation_status: not_run
source_ids: []
knowledge_ids: []
retry_of: null
elapsed_seconds: null
input_tokens: null
cached_input_tokens: null
---

# 运行摘要

- 用户目标：
- 处理范围：
- 结果概览：
- 轨迹说明：live 表示执行时记录；reconstructed 表示事后重建，必须说明依据和不可恢复的信息。

# 输入与抓取

| Source ID | 来源 | 完整性 | 获取方式 | 正文载入次数 | 证据边界 |
|---|---|---|---|---:|---|
| src-... | [标题](../../sources/YYYY/file.md) | complete | metadata_and_digest | 未记录 | 说明来源质量与缺口 |

# 候选命题决策表

| ID | 候选命题 | Source IDs | 证据强度 | 已有匹配与实质变化 | 决策 | 目标 | 理由 |
|---|---|---|---|---|---|---|---|
| C01 | 可独立理解的命题 | src-... | low | 无匹配或说明新增差异 | CREATE | kn-... | 说明为何这样处理 |

# 写入映射

记录每个 Source、Knowledge、Catalog 的 CREATE、REINFORCE、UPDATE、CONFLICT 或无写入结果，并关联候选 ID。

# 质量检查

- 重复节点风险：
- 弱匹配：
- 单一来源 CREATE：
- 外部证据覆盖：
- 决策分布：

# 调试信号与未解决问题

- 哪些判断最不确定：
- 哪些候选可能分错节点：
- 下次应观察什么指标或反证：
- 时间、token、缓存或正文载入次数不可得时写“未记录”，不要估算。

# 验证结果

- 统一校验：not_run
- Git 差异：未检查
- 警告与失败：

# Review 记录

- 尚未 Review。
