---
id: src-20260811-lance-multimodal-agent-lake
title: 从多模态数据湖到 Agent 湖：Lance 的格式设计与实践
source_type: article
author: 马进（演讲者）；Lance & LanceDB（公众号）
source_date: 2026-08-11
imported_at: 2026-08-16
original_location: https://mp.weixin.qq.com/s/vDohyhtAGJKX-LWcOnHbJQ
original_url: https://mp.weixin.qq.com/s/vDohyhtAGJKX-LWcOnHbJQ
canonical_url: https://mp.weixin.qq.com/s/vDohyhtAGJKX-LWcOnHbJQ
retrieved_at: 2026-08-16
capture_mode: metadata_and_digest
access_status: complete
content_sha256: 3c8c4aca6b9dc1e4cb0e69aa78762e38463dee97f15b47df6d6c16c24c5825a2
content_hash_scope: wechat_js_content_text
status: archived
---

# 来源说明

- 资料性质：微信公众号技术文章，主体为 2026 AICon 全球人工智能开发与应用大会演讲实录。
- 获取方式：2026-08-16 从用户提供的微信 URL 直接获取页面 HTML，并读取 `#js_content` 正文区域。
- 完整性：已取得从开篇到结尾的正文，约 5,460 个文本字符；未保存配图，也未复制第三方全文。
- 抓取状态：complete。
- 保存范围：出处、正文哈希、结构化摘要和知识判断所需的产品主张。
- 一手/二手属性：可视为演讲者和项目相关账号对 Lance 定位与设计意图的一手说明；对客户效果和性能数字不是独立验证。
- 可信度提示：适合了解 Lance 的架构主张、适用场景和产品定位。文章来自项目相关账号并包含产品推广倾向，具体性能、生产成熟度和客户收益仍需基准测试、用户案例或官方技术文档交叉核验。

# 结构化内容摘要

## 问题背景

AI 数据需要同时支持 ETL 与分析、模型训练、样本回放、向量与全文检索、评测、打标和 Agent 记忆。多模态场景还会把文本、图片、视频、点云、传感器、标签、embedding、模型得分和实验版本放在同一条数据链路中。若这些对象分散在对象存储、向量库、全文检索、训练文件和元数据库，复用成本、一致性风险和链路复杂度会上升。

## Lance 的定位与设计

文章把 Lance 定位为面向 AI 数据底座的 lakehouse format stack，而不是单纯的向量数据库：

- File Format 通过 column pages、offsets 和 footer 优化随机访问路径；
- Table Format 通过 fragments、versions 和事务能力进行表级治理；
- Index Formats 覆盖向量、全文和标量索引；
- Catalog 与 Namespace 负责表发现、多引擎协同和接入。

文章认为，多模态 AI workload 的主要格式诉求是：大宽表、低成本结构变更、结构化与非结构化对象混合管理，以及低成本随机点查。Lance 通过独立追加 DataFile 支持加列，通过 Blob V2 管理大对象，并把索引、版本、分支和 Tag 等能力向格式层下沉。

## 与传统湖格式的关系

文章没有把 Lance 描述为 Parquet、Iceberg、Delta 或 Paimon 的全面替代品。传统格式继续适合结构化分析、快照、事务演进和成熟的多引擎治理；Lance 主要补充训练、检索、评测、打标、频繁加列、多模态对象和随机访问等 AI workload。实际 pipeline 可以在上游继续使用 Iceberg 等格式治理，再加工为 Lance 表服务下游 AI 任务。

## Agent 记忆与上下文

文章把 Agent Memory 描述为从对话和操作中捕获、切分、向量化、索引并在后续任务中召回的信息。进一步的判断是：Memory 可能只是 Context 中高质量、个性化内容的提取结果；Context 还包括文档、图片、视频、代码、历史决策、工具调用结果、检索日志和跨会话引用，因此是更完整的数据资产。

# 来源声称但尚未独立核验的指标

- 特定随机读取场景可把读取路径压缩到 1—2 次 IOP，并相较 Parquet 获得数量级提升；
- 某智驾案例中点云和图片压缩后约为原始数据的 30%，并支撑当年超过 10 倍的数据增长；
- 某 Agent 记忆插件实践中，记忆捕获增强 30%，召回准确率提升 20%。

文章未提供足以复现这些数字的完整基线、数据集、硬件配置、测试方法和统计口径，因此本次不把它们写成 Knowledge 的当前结论。

# 可长期沉淀的候选认知

1. AI 数据底座不应按产品名称选型，而应由数据模态、访问模式、结构演进、索引需求、版本治理和现有生态共同决定。
2. Agent 记忆应被看成完整上下文资产的派生视图；只保存摘要或 embedding 会削弱追溯、重算和纠错能力。

# 内容哈希说明

`content_sha256` 对应抓取页面中 `#js_content` 正文节点的文本值，用于后续重复检测和来源变化识别；仓库中只保存结构化摘要，不保存第三方全文。

