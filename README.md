# Personal KB

一个基于 Markdown 与 Git 的可演进个人知识库。

它不以“保存了多少文章”为目标，而以这件事为目标：

> 在真正遇到问题时，能召回相关、可追溯、不过时且有适用边界的知识，帮助形成更好的判断。

## 目录

~~~text
personal_kb/
├── AGENTS.md                    # Codex 的仓库级行为规则
├── inbox/                       # 待处理材料
├── ingest_runs/YYYY/            # 每次入库的决策、写入与验证记录
├── sources/YYYY/                # 原始资料快照与出处
├── knowledge/<topic>/           # 持续演进的知识节点
├── index/catalog.md             # 问题到知识文件的轻量索引
├── templates/                   # Source / Knowledge / Ingest Run 模板
└── .agents/skills/personal-kb/  # INGEST / ASK / REVIEW 工作流
~~~

## 如何使用

最省事的方式，是从本仓库打开 Codex 后直接说自然语言：

~~~text
把 /某个路径/文章.md 融入我的知识库。

https://mp.weixin.qq.com/s/文章链接

结合我的知识库，分析我该如何改善和金钱的关系。

复查“心理预演”主题，列出现有结论、来源、冲突和证据缺口。

复查 ingest_runs/2026/2026-08-16-wechat-five-articles.md，检查候选命题和节点匹配是否合理。
~~~

也可以沿用三种简短意图：

~~~text
/ingest
把新信息融入我的认知体系

/ask
结合我的已有认知回答问题

/review
检查某个主题当前的认知、冲突和来源
~~~

需要可靠地显式调用 Skill 时，在 Codex CLI 或 IDE 中使用：

~~~text
$personal-kb /ingest /绝对路径/文章.md
$personal-kb /ask 我该怎样理解显化与现实行动的关系？
$personal-kb /review 财富、价值创造与信任
~~~

在支持 Skill 选择器的桌面界面中，选择“个人知识库”后输入同样的任务即可。Skill 也允许隐式触发，因此一般不必每次点名。

> 说明：OpenAI 已将自定义 Slash Prompt 标为弃用，并建议用 Skills 承载可复用工作流。因此 /ingest、/ask、/review 在这里是稳定的意图约定，而不是额外安装的旧式自定义命令。

### URL 与微信公众号文章

在本仓库的对话中，只发送一个 URL，默认等同于 /ingest。流程会：

~~~text
读取完整正文与元数据
→ 检查 URL 或内容是否已经入库
→ 保存可追溯 Source 记录
→ 与已有 Knowledge 比较
→ CREATE / REINFORCE / UPDATE / CONFLICT / IGNORE
~~~

微信公众号可能出现登录、反爬或正文动态加载。如果无法取得完整正文，系统不会用标题或搜索摘要强行入库，而会请你粘贴全文、上传导出文件或 PDF。

第三方公开网页默认保存 URL、作者、日期、结构化内容摘要和必要短引用，不复制整篇受版权保护的正文。你直接粘贴、上传或明确拥有权利的材料可以保存完整快照。

## 三种模式做什么

### INGEST

~~~text
读取资料
→ 搜索现有 Knowledge
→ 持久化候选命题决策表
→ 逐条判断 IGNORE / CREATE / REINFORCE / UPDATE / CONFLICT
→ 保存 Source 快照
→ 更新 Knowledge
→ 更新 catalog
→ 记录写入映射、质量信号与验证结果
~~~

每次 INGEST 都会在 `ingest_runs/YYYY/` 留下可审查记录。它展示资料如何被拆成候选命题、与哪些已有节点匹配、为何创建或忽略、最终改了哪些文件，以及还有哪些弱匹配和证据缺口。该目录用于调试入库逻辑，不参与默认 ASK 召回。

统一校验还会聚合各次运行的 CREATE 比例、弱匹配、单一来源新建、外部验证覆盖和警告数量，用于判断知识库是否正在无序膨胀。

### ASK

~~~text
读取 catalog
→ 选择 1—5 个相关知识节点
→ 检查状态、时效性和边界
→ 把知识库作为 Prior
→ 结合当前情境回答
~~~

默认不修改知识库。

### REVIEW

~~~text
聚合某个主题的知识节点
→ 回溯 Source
→ 检查重复、冲突、过期和证据缺口
→ 给出当前认知与下一步验证建议
~~~

默认不修改知识库；需要合并或修正时再明确发起 INGEST。

## 入库决策

- IGNORE：没有长期价值，或完全重复且不增加证据。
- CREATE：出现新的、可独立复用的知识命题。
- REINFORCE：增加了已有结论的证据、解释或应用。
- UPDATE：需要修改已有结论、边界、置信度或方法。
- CONFLICT：与已有知识存在重要矛盾，暂时保留争议。

## 如何修改已有知识

推荐直接在对话里说出修正内容，例如：

~~~text
$personal-kb /ingest
关于“显化”，我现在更准确的认知是：……
请更新相关知识，并保留原来的来源和演进记录。
~~~

系统会把你的新表述保存为 user_reflection Source，然后判断是 CREATE、REINFORCE、UPDATE 还是 CONFLICT。旧 Source 不会被覆盖，因此以后可以追溯“认知为什么改变”。

也可以直接编辑 knowledge/ 下的 Markdown，但不要手动改写 sources/ 中已经归档的 Source。手动修改后建议运行：

~~~text
$personal-kb /review 检查刚才修改的主题、来源链、冲突和 Catalog
~~~

如果某条认知不再采用，应标记 deprecated 或 superseded，而不是删除历史证据。

## 当前阶段

这是 v0.1：使用 Markdown、Git、目录索引与一个仓库级 Skill，不引入数据库、Embedding 或独立 RAG 服务。先用真实资料验证知识摄入和未来回答是否明显变好，再决定是否升级检索基础设施。

其中，last_verified_at 只说明在 verification_scope 所写范围内完成过检查；external_evidence_status 才说明是否核过外部证据。二者不能混为一谈。
