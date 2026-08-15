# Knowledge Catalog

本目录用于把用户问题映射到少量相关 Knowledge。它是轻量检索入口，不代替 Knowledge 正文。

## AI 与数据系统

### AI 系统优化应优先核算数据搬运与低延迟成本

- Path: knowledge/ai-infrastructure/ai-system-optimization-starts-with-data-movement.md
- 一句话：数据在内存层级、加速器和芯片间移动的成本常会主导 AI 系统；batching 能提高吞吐却损害交互延迟，训练与在线推理应分别按真实负载建模。
- 适合回答：
  - 为什么 AI 系统不能只看 FLOPs？
  - batching 为什么提高效率却损害低延迟？
  - 推理服务和专用硬件应该测哪些指标？
  - 什么时候值得为工作负载做硬件专用化？
- Tags: 数据搬运, HBM, batching, 推理延迟, 能效, 互连, 专用硬件
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16

### AI 数据底座的格式选择应由访问模式驱动

- Path: knowledge/ai-data/ai-data-format-follows-access-patterns.md
- 一句话：结构化分析继续优先使用成熟湖格式；当多模态 AI 数据需要频繁加列、随机访问、混合索引和实验版本管理时，再评估 Lance 一类 AI-native 格式作为补充。
- 适合回答：
  - 什么时候需要 AI-native 数据格式？
  - Lance 与 Parquet、Iceberg 是替代还是互补关系？
  - 同一份数据同时服务训练、检索和分析时应该如何选型？
  - 多模态数据湖架构应该重点评估什么？
- Tags: Lance, LanceDB, 数据湖, Lakehouse, 多模态, Parquet, Iceberg, 随机访问, Schema 演进, 向量检索
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16

### Agent 记忆应被视为上下文资产的派生视图

- Path: knowledge/ai-agents/agent-memory-is-derived-from-context.md
- 一句话：Memory 是从完整 Context 中选择、压缩和索引得到的派生视图；在合规与成本允许的范围内保留来源、版本和关系，才能支持纠错、重算和审计。
- 适合回答：
  - Agent Memory 和 Context 有什么区别？
  - 为什么不能只保存摘要和 embedding？
  - Agent 长期记忆系统应该怎样分层？
  - 如何让 Agent 的记忆可追溯、可纠错和可重算？
- Tags: Agent Memory, Context, 上下文资产, 记忆, 来源追溯, 版本, 检索, embedding
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16

### Agent 长任务可靠性来自规格、技能与评估闭环

- Path: knowledge/ai-agents/agent-reliability-needs-spec-skills-evaluation-loop.md
- 一句话：长任务 Agent 需要清晰规格、可执行 skills、可观测状态、可信评估和失败恢复共同闭环；企业生产还要补齐数据、权限、审批、日志与分阶段上线。
- 适合回答：
  - 怎样让 Agent 稳定执行长链路任务？
  - Agent 为什么在多步执行后容易跑偏？
  - Skills、工具和评估器分别解决什么问题？
  - 如何判断一个 Agent 工作流是否真正进入生产？
- Tags: Agent, Context Engineering, Skills, 规格, 工具调用, 评估器, 审批, 分阶段上线, 长任务
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16

### 企业 Agent 的产品单元应是可验收的工作结果

- Path: knowledge/ai-products/enterprise-agent-product-is-verifiable-work.md
- 一句话：优先把企业已经付费、反复发生、结果清楚且可人工接管的一段工作做成 Agent，再从辅助、分流和受限动作逐步扩大授权。
- 适合回答：
  - 企业客户为什么愿意为 Agent 付费？
  - 什么工作适合做成第一版 Agent？
  - “AI 员工”和传统 SaaS 的产品单元有什么不同？
  - 什么时候可以采用结果计费？
- Tags: 企业 Agent, Agent SaaS, AI 员工, Workflow, 工作结果, 结果计费, 人工接管, ROI
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16

### AI 产品切入口必须经受通用模型进步检验

- Path: knowledge/ai-products/ai-product-wedge-must-survive-model-progress.md
- 一句话：不要把基础模型今天的能力缺口或 AI 带来的执行提速直接当作护城河；应同时测试真实价值、能力趋势、持久资产和下一组可证伪证据。
- 适合回答：
  - 怎样判断一个 AI 产品方向会不会很快被基础模型覆盖？
  - 模型成功率很低是否意味着存在创业机会？
  - 小团队相对通用模型还能建立什么优势？
  - AI 降低执行成本后，创业者应该把时间投向哪里？
- Tags: AI 产品, 1% 法则, 通用模型, 模型进步, 执行成本, 私有数据, 工作流, 护城河, 下一证据
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16

### 自动化实验的扩展上限常由评估器决定

- Path: knowledge/ai-systems/automated-experimentation-is-bounded-by-evaluator.md
- 一句话：候选生成变快后，目标可度量性、评估速度和评估真实性会成为自动化实验的主要约束；近似评估器必须持续接受真实结果校准。
- 适合回答：
  - 什么问题适合用 Agent 自动跑大量实验？
  - 为什么生成候选很快，研发闭环仍然很慢？
  - 近似评估器应该怎样使用？
  - 如何防止自动化系统优化错误指标？
- Tags: 自动化实验, 评估器, surrogate model, 科学方法, 搜索, Goodhart, Ground Truth, 研发闭环
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16

## 自动驾驶与物理 AI

### 物理 AI 的代理任务是训练脚手架，不是最终产品指标

- Path: knowledge/autonomous-driving/proxy-tasks-are-training-scaffolding.md
- 一句话：当高维感知到低维动作的主任务严重欠约束时，几何、分割、深度、光流或 OCR 等代理任务可增加监督并约束表征，但不能自动证明因果、可解释或安全。
- 适合回答：
  - 端到端自动驾驶为什么还需要检测、分割、深度等任务？
  - 高维视频到低维动作为什么容易学到捷径？
  - 代理任务指标和最终驾驶指标是什么关系？
  - 代理任务能否证明模型具有因果性或可解释性？
- Tags: 端到端, 代理任务, Multi-task Co-training, 稠密监督, 捷径学习, 表征学习, 闭环评测
- Status: active
- Confidence: low
- External evidence: not_checked
- Last verified: 2026-08-16

### 物理 AI 数据闭环应优化信息增益，而不是随机堆量

- Path: knowledge/autonomous-driving/data-engine-optimizes-information-gain.md
- 一句话：围绕模型分歧、人工接管、低置信度、新颖场景和风险事件采样，并保留代表性基线、标签来源和闭环回归，通常比只增加总里程更有价值。
- 适合回答：
  - 自动驾驶数据应该怎样采样才更有效？
  - 模型与人类行为分歧为什么值得回收？
  - 离线教师模型生成标签要控制什么风险？
  - 车队规模是否会让边缘案例问题消失？
- Tags: 数据引擎, Active Learning, Disagreement Mining, Hard Example Mining, 人工接管, 离线标注, 教师模型
- Status: active
- Confidence: low
- External evidence: not_checked
- Last verified: 2026-08-16

## 组织与管理

### AI 扩大个体产出后，组织瓶颈会转向系统一致性与专业责任

- Path: knowledge/management/ai-output-shifts-bottleneck-to-system-accountability.md
- 一句话：AI 让原型、代码和分析更便宜后，组织优势更多取决于问题选择、生产门槛、共享平台、跨团队一致性和对最终结果负责，而不是局部产出数量。
- 适合回答：
  - AI 让人人都能做原型后，组织为什么不一定更快？
  - 系统型人才在 AI 时代为什么更重要？
  - 跨职能是否意味着专业分工会消失？
  - AI 熟练度应该怎样定义和培养？
- Tags: 系统思维, 专业能力, 原型, 平台, 护栏, AI 熟练度, 责任, 人才密度
- Status: active
- Confidence: low
- External evidence: not_checked
- Last verified: 2026-08-16

## 个人成长

### 显化可以操作化为目标、差距、内在对齐与行动反馈

- Path: knowledge/personal-development/manifestation-goal-gap-alignment-action.md
- 一句话：先定义具有画面感且可观察的目标，再评估现实差距，觉察并调整显性的想法与隐性的情绪反应，然后围绕目标行动并用反馈迭代。
- 适合回答：
  - 显化的核心到底是什么？
  - 怎样把一个愿望变成可以开干的目标？
  - 负面情绪与潜意识是什么关系？
  - 目标、现实差距和行动应该怎样结合？
- Tags: 显化, 目标, 现实差距, 意识, 潜意识, 感觉, 负面情绪, 行动
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16

### 信念通过感受、注意与行动形成自我强化循环

- Path: knowledge/personal-development/belief-emotion-attention-action-loop.md
- 一句话：信念不会被假定为直接创造所有外部事件，但会通过解释、感受、注意、选择、互动和行动影响结果，而结果又会反过来强化信念。
- 适合回答：
  - 为什么我明知应该行动，却总回到旧模式？
  - 情绪出现时，如何找到背后的信念？
  - 怎样把“显化”理解为可执行的改变循环？
- Tags: 信念, 情绪, 注意力, 行动, 反馈循环, 显化
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16

### 心理预演应与现实行动和反馈配合

- Path: knowledge/personal-development/visualization-must-pair-with-action.md
- 一句话：视觉化更适合作为澄清目标、调节状态和预演行动的工具，不能被当作保证外部结果或替代现实行动的机制。
- 适合回答：
  - 视觉化练习到底有什么用？
  - 怎样做不脱离现实的“显化”练习？
  - 肯定语和冥想为什么有时没有效果？
- Tags: 视觉化, 心理预演, 目标, 冥想, 行动, 反馈
- Status: active
- Confidence: low
- External evidence: not_checked
- Last verified: 2026-08-16

## 财富与商业

### 长期财富依赖价值、信任与持续交付

- Path: knowledge/wealth/wealth-depends-on-value-trust-and-delivery.md
- 一句话：对多数可持续收入而言，关注为谁创造什么价值、如何获得信任并持续交付，比只强化“我想要钱”更可执行；但市场结构、资源、运气和财务管理同样重要。
- 适合回答：
  - 应该怎样建立更健康的财富观？
  - 追求收入增长时，应该优先关注什么？
  - 利他、价值创造与商业回报是什么关系？
- Tags: 财富, 价值创造, 信任, 持续交付, 收入, 商业
- Status: active
- Confidence: medium
- External evidence: not_checked
- Last verified: 2026-08-16
