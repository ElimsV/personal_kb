---
id: src-20260816-agent-saas-sells-work
title: AI Agent 就是新一代 SaaS
source_type: article
author: Capihom（公众号：晚点再听 LaterCast）
source_date: 2026-07-07
imported_at: 2026-08-16
original_location: https://mp.weixin.qq.com/s/a_kmAg0XM0SKNpVev_ePyA?scene=334
original_url: https://mp.weixin.qq.com/s/a_kmAg0XM0SKNpVev_ePyA?scene=334
canonical_url: https://mp.weixin.qq.com/s/a_kmAg0XM0SKNpVev_ePyA
retrieved_at: 2026-08-16T01:42:23+08:00
capture_mode: metadata_and_digest
access_status: complete
content_sha256: 742ce00bed69540ed1c57f471fea6c1cdebcad393b3916a97e664edf4e55a45a
content_hash_scope: normalized_rendered_article_body
status: archived
---

# 来源说明

- 资料性质：对 Greg Isenberg 的 Startup Ideas Podcast 节目的中文二次整理，偏创业方法和产品建议，不是市场统计或经验证研究。
- 获取方式：下载公开微信页面 HTML，并从 `#js_content` 提取完整渲染正文及页面元数据。
- 完整性：正文提取完整；正文规范化后约 4,756 个字符。
- 抓取状态：complete。
- 保存范围：仅保存出处、结构化内容摘要和必要短引，不保存第三方全文。
- 可信度提示：文章给出原视频 `https://www.youtube.com/watch?v=83fWzQSWB10`，本次未对照核验；定价示例和 30 天计划属于启发式建议，不代表普遍可行或已验证回报。

# 结构化内容摘要

## 从卖软件转向接手一份工作

- 文章用“SaaS 卖软件，Agent SaaS 卖工作”概括产品单位的变化：客户不只购买操作界面，而是把一段原本由员工或外包完成的工作交给系统。
- 适合的起点是企业已经付出工资、外包、漏单或协调成本的流程，且高频、结果明确、能访问既有软件、预算所有者清楚。
- 太简单的任务容易被规则自动化覆盖；太依赖模糊人类判断的任务不适合首版。甜点区是重复、烦琐、带少量判断且可验收的工作。

## 先观察真实工作，再定义 Agent

- 在设计前观察员工连续执行同类任务，记录触发条件、上下文来源、工具顺序、异常和升级路径。
- Agent spec 至少应写清触发器、上下文、工具、可自主动作、批准点、转人工条件和成功标准。
- 先把可预测部分实现为 workflow，只在判断能创造价值的环节使用 Agent 动态决策。

## 最小有用形态与信任外壳

- 首版可以从起草后批准、入口分流、跨系统协调或规则内的限定动作开始，而不是追求完全自主。
- 控制台、日志、审批、设置、分析、交接和上线前评测构成信任外壳；客户需要看到 Agent 做了什么、为何这么做、错误如何处理。
- 用历史真实案例组成 eval set，每次更换 prompt、模型、工具或流程后回归，是把产品承诺变成可复查证据的方式。

## 从服务试点沉淀软件

- 早期可为同一细分行业的少量客户手工交付同一个 workflow，用试点学习真实痛点、失败方式、审批边界和客户语言，再逐步产品化。
- 设置费、月费、使用量和结果计费都可作为探索方式；结果计费应等价值归因、基线和风险分配更清楚后再采用。
- 文章建议用旧流程与 Agent 新流程的对比展示产品价值，但营销案例不能替代真实运行数据。

# 可提炼命题

- 企业 Agent 的最小产品应是一段可验收、可接管、有既存成本的工作，而不是一个泛化聊天入口或宏大平台。
- 生产可信度来自真实流程观察、明确 Agent spec、历史案例评测、日志审批和渐进式授权；模型新颖度不是客户采用的充分条件。

# 证据缺口与潜在伤害

- 未核对原播客，也没有独立证据证明文中定价、销售路径或 30 天节奏适合所有行业。
- 自动处理电话、退款、预约和工单会带来身份、隐私、授权、错误补救和消费者告知问题。
- 结果计费若归因不清，容易诱导短期优化、选择性服务或客户争议。
- “卖工作”可能忽视员工转岗、监督劳动、模型错误责任和高风险流程中不可替代的人类判断。

# 入库决策

1. CREATE：`kn-20260816-enterprise-agent-product-verifiable-work`，与瓴羊访谈共同支持“可验收工作结果”作为产品单元。
2. REINFORCE：`kn-20260816-agent-reliability-spec-skills-evaluation`，补入真实流程观察、Agent spec、历史案例评测、日志与渐进授权。
3. REINFORCE：`kn-20260816-ai-product-wedge-survive-model-progress`，把既存成本、高频、可验收 workflow 和同类客户试点作为方向验证方法。
4. IGNORE：定价锚点和 30 天计划不升级为普遍方法或效果事实，只保留为待验证启发式。
