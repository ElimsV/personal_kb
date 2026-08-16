# Personal Knowledge Base Instructions

## 目标

这个仓库是用户拥有的个人知识库。它保存可追溯、可检索、能持续修正的认知，而不是文章收藏夹或摘要堆。

默认使用中文。保留必要的英文术语、文件名和机器标识。

## 知识库是 Prior，不是 Truth

- 把 knowledge/ 中的内容视为用户当前的认知基线，不把它当作不容质疑的事实。
- 始终区分：来源说了什么、当前知识节点如何判断、这次回答基于新情境得出什么。
- 不因内容被收藏就提高可信度；结合来源质量、confidence、freshness、status 和适用边界判断权重。
- 遇到新证据与现有知识冲突时，明确指出冲突，以更可靠、更新且更适用于当前问题的证据为准。
- 对 fast 或 very_fast 的事实性知识，如果问题要求当前结论，先核验最新信息。
- last_verified_at 必须结合 verification_scope 和 external_evidence_status 解读；核对过 Source 不等于已完成外部事实或科学验证。

## 三种工作模式

用户可以用自然语言，也可以在消息开头使用以下意图标记：

- /ingest：把新资料融入认知体系。使用 $personal-kb Skill 的 INGEST 流程。
- /ask：结合已有认知回答问题。先读 index/catalog.md，再读取 1—5 个真正相关的知识文件。
- /review：检查一个主题的当前结论、来源、冲突、时效性与认知缺口。
- 当用户只发送一个 http/https URL，且没有表达其他意图时，默认按 /ingest 处理；微信公众号文章同样适用。

这些标记是本仓库的对话约定，不依赖已弃用的自定义 Slash Prompt。若所在界面不接受未知 / 命令，改用 $personal-kb /ingest ...、$personal-kb /ask ...、$personal-kb /review ...，或直接用自然语言表达。

## 默认读取规则

当用户提出可能与个人知识库有关的分析、决策、管理、产品、商业、AI、个人成长或生活问题时：

1. 先查看 index/catalog.md。
2. 只读取与问题明显相关的知识文件，不为使用知识库而强行引用。
3. 检查知识节点的状态、置信度、时效性、来源与适用边界。
4. 回答时优先给出针对当前问题的结论，再说明哪些判断来自知识库、哪些是本次推断或外部核验。
5. 除非用户要求入库，否则 ASK 和 REVIEW 默认只读；可以建议沉淀，但不要擅自修改知识库。

## 写入规则

- 收到入库请求时，必须使用 .agents/skills/personal-kb/SKILL.md。
- 所有会修改 ingest_runs/、sources/、knowledge/ 或 index/catalog.md 的 INGEST 都必须遵守仓库写锁；资料抓取可并行，最终决策与知识库写入必须串行。锁的获取、心跳、释放和异常处理以 Skill 为准。
- URL 来源必须读取正文而不是只看标题、搜索摘要或转述。若登录、反爬或动态渲染导致正文不完整，应尝试浏览器读取；仍不完整时停止知识更新，请用户粘贴全文、上传文件或导出 PDF。
- 先搜索 index/catalog.md 和 knowledge/，再决定 IGNORE / CREATE / REINFORCE / UPDATE / CONFLICT。
- 一篇 Source 可以支持多个 Knowledge；多篇 Source 也可以共同维护一个 Knowledge。
- 不默认执行“一篇资料创建一篇知识总结”。优先强化或修正已有知识，避免重复节点。
- Source 快照写入 sources/YYYY/；建立后原则上不改正文。原资料发生变化时新建版本，并记录哈希和关系。
- 用户直接提供或拥有权利的内容可以保存完整快照；第三方公开网页默认只保存出处、结构化内容摘要和必要的短引用，不复制整篇受版权保护的正文。
- Knowledge 写入 knowledge/<topic>/；每个文件只维护一个可独立理解的核心命题。
- 每次 Knowledge 变化都更新演进记录，并同步 index/catalog.md。
- 每次 INGEST 都在 ingest_runs/YYYY/ 保存运行日志，包括完整候选命题决策表、写入映射、质量信号、失败与验证结果；即使全部 IGNORE 或抓取失败也要留痕。
- 已完成运行日志保留原始决策。复查后的修正追加带日期的 Review 记录，或新建通过 retry_of 关联的运行日志，不静默改写原决策。
- 不把作者观点自动升级为事实，不补写来源中没有的内容，不用故事、类比或个案替代证据。
- 未经用户明确要求，不自动提交 Git，不推送远端。
- 用户对已有认知的补充、修正或反对意见也应先保存为新的 user_reflection Source，再更新 Knowledge；不要回写或删除旧 Source。

## 目录职责

- inbox/：待处理材料，可被清空，不是长期知识。
- ingest_runs/：持久化的入库运行记录，用于复查决策、调试流程和观察质量趋势，不参与默认知识召回。
- sources/：不可变的来源快照与出处信息。
- knowledge/：持续演进的当前认知节点。
- index/catalog.md：面向问题召回知识的轻量索引。
- templates/：Source、Knowledge 与 Ingest Run 的统一格式。
- .agents/skills/personal-kb/：INGEST、ASK、REVIEW 的操作流程。

## 质量底线

- 重要结论必须能追溯到 Source，或明确标为用户经验/本次推断。
- 事实、经验、观点、方法与推测不得混写。
- 明确写出成立条件、不适用场景、反例与可能伤害。
- 区分“Source 快照完整”“知识节点忠实于 Source”和“命题已获外部证据支持”三种不同验证。
- 涉及医疗、法律、投资、重大财务决策等高风险主题时，知识库不能替代当前专业核验。
- 检查 Git 差异和内部链接后，再声称入库完成。
