# 全量多模态会议深度处理宪法（用户原文，逐字保留）

> 本文件是任务的最高优先级规则原文。SKILL.md 是其可执行摘要；两者冲突时以本文件为准。

你现在需要对我本次提供的全部会议相关材料进行完整、多模态、无遗漏的深度处理，并最终输出且只能输出一份 Markdown（.md）文件。
这一份 Markdown 文件必须同时包含：

- 完整、细致、深入理解后的会议纪要
- 完整中文逐字稿 / 逐字译稿
- 必要的投屏内容重建
- 必要的视觉材料结构化还原
- 文件处理完整性审计
- 必要的异常说明与信息冲突说明
  禁止把会议纪要、逐字稿、投屏内容或审计结果拆成多个独立文件。
  最终只允许存在一份完整会议 Markdown 文件。

## 一、最高优先级原则：全量处理宪法

这是整个任务的最高优先级规则。
我本次上传、提供、指定或当前工作环境中属于本次会议的所有材料，一个都不允许跳过。
包括但不限于：音频、视频、会议录屏、PPT / PPTX、PDF、Word / DOCX、Excel / XLSX、CSV、图片、截图、TXT、Markdown、已有 Transcript、已有会议纪要、Summary、Meeting Notes、聊天记录、邮件、附件、其他任何与本次会议有关的材料。
必须首先识别全部输入材料，并建立完整的 File Inventory。之后逐个进行处理。

绝对禁止因为任何理由跳过文件。以下理由都不能成为跳过文件的理由：
- “已经有 Transcript，所以不需要再听音频。”——错误。
- “视频和音频内容一样，所以只需要处理一个。”——错误。
- “PPT 已经在视频中出现，所以独立 PPT 文件不需要再读取。”——错误。
- “已经有 Summary，所以可以直接生成纪要。”——错误。
- “这个附件好像不重要。”——错误。
- “几个文件看起来高度重复。”——仍然必须全部处理。
- “内容很多，为了节省 Token 可以忽略一部分。”——绝对禁止。

## 二、原始材料优先原则

证据优先级：原始音频 / 原始视频 / 原始文件 → 已有 Transcript / OCR / 自动识别结果 → 已有 Meeting Notes / Summary / 二手整理内容。
已有 Transcript、Summary、Meeting Notes 等可以用于：辅助识别、辅助定位、补充线索、交叉验证。但是绝不能替代原始材料。最终事实判断必须尽可能回到原始 Source。

## 三、音频必须完整处理

所有音频文件必须从第一秒处理到最后一秒。不能只抽取部分区间。不能因为已经存在 Transcript 而不处理原音频。
如果同时存在 Audio、Transcript、Summary，则必须全部阅读/处理，并进行交叉验证。
重点校验：发言内容、漏句、错字、人名、团队名、项目名、产品名、系统名、公司名、地区名、专有名词、内部黑话、英文术语、葡萄牙语/西班牙语等其他语言、数字、金额、百分比、日期、时间、Deadline、缩写、中英文混说、发言人身份。
如果无法可靠确认：[听不清 00:23:17]。如果存在较高概率判断但不能确定：[疑似：“XXX” 00:23:17]。不能为了让句子好看而编造。

## 四、视频必须真正“看完”，而不是只处理音轨

所有会议视频/会议录屏必须从第一秒看到最后一秒。视频必须同时处理两个 Channel：
- Audio Channel：完整处理会议中的所有语音内容。
- Visual Channel：持续检查会议画面，包括但不限于：Screen Share、PPT、Excel、Spreadsheet、Word、PDF、Dashboard、Jira、Roadmap、Timeline、Project Plan、流程图、架构图、原型、产品页面、后台系统、数据看板、IM、聊天记录、邮件、表格、数据、图表、图片、截图、白板、SQL、Code、Browser、文档、会议聊天框、任何其他视觉信息。

禁止：只提取视频音频 → 转写 → 把它当成已经处理完视频。这不算完整处理视频。

## 五、会议中的投屏内容必须被完整信息化

如果会议过程中出现 Screen Sharing，不能简单写“此处展示 PPT”或“此处展示了一张 Excel”。
需要尽最大能力把画面中的实际信息转成：Markdown、Structured Text、Markdown Table、Key-Value Structure、Hierarchical Text、ASCII Diagram、Mermaid、其他适合 AI 理解的结构。具体使用哪种形式，由你根据内容自行判断。
核心标准只有一个：即使未来完全无法访问原始会议录屏，仅仅读取最终 Markdown，也应该能够最大程度理解当时屏幕上展示了什么。

## 六、视觉内容不要机械 OCR，要理解结构

不要只是把屏幕上的字 OCR 出来。还需要理解：标题和正文是什么关系、行和列是什么关系、哪些字段属于同一条记录、哪些数字对应哪个 Metric、哪些内容属于同一项目、哪些内容是 Owner、哪些内容是 Deadline、箭头代表什么关系、流程从哪里到哪里、上下游是什么、图例代表什么、Status Color 代表什么、页面中哪些内容被会议参与者重点讨论、Speaker 当前说的话对应屏幕上的哪个位置。
对于表格，尽可能恢复表格结构。对于流程图/架构图，尽可能恢复节点和连接关系。对于 PPT，尽可能恢复页面结构。对于 Dashboard，尽可能恢复指标与数据之间的关系。
对于图表，尽可能恢复：Axis、Legend、Series、Unit、Time Range、Data、Trend、Annotation。
但必须区分：画面客观展示的信息、会议参与者对画面的解释、AI 自己根据画面进行的推断。三者不能混为一谈。

## 七、使用现有知识资料进行深度交叉验证

在处理本次会议时，可以并且应该结合当前可访问的现有知识资料进行交叉验证和上下文理解。
可以查阅：同项目历史材料、历史会议记录、项目文档、项目背景、相关流程、历史 Decision、历史 Action、历史 Timeline、术语定义、项目成员信息、系统关系、产品关系、业务背景、组织关系、其他能够帮助理解当前会议的资料。
目标是帮助解决：这个缩写到底指什么、Speaker 提到的“上次那个问题”是什么、某个项目名称是否识别正确、某个人名是否听错、某个系统属于什么模块、某个数字对应什么业务指标、某个 Decision 是新 Decision 还是历史 Decision、某个问题是本次第一次提出还是历史遗留、某个 Timeline 与此前计划是否存在变化、某个讨论为什么会发生。

但是必须遵守 Source Boundary：现有资料的作用是理解 + 验证 + 补充上下文。不能因为现有资料中存在某个信息，就默认这个信息在本次会议中被说过。必须严格区分：本次会议明确出现的信息、其他已有资料提供的背景、AI 基于多源证据做出的判断。三者不能混淆。如果引用已有资料补充重要背景，应该让读者能够明确知道：这是背景信息，而不是本次会议中新产生的信息。

## 八、禁止对任何现有资料进行主动修改

本任务对现有资料的使用方式是 Read / Search / Understand / Cross-Validate，而不是 Write / Update / Modify / Reorganize。
除非我另外明确要求，否则不要主动修改、更新、覆盖或重构任何现有资料。本任务唯一主要输出是：本次会议最终完整 Markdown 文件。

## 九、必须进行真正的跨来源验证

所有相关 Source 应结合起来理解，而不是各自孤立处理：Audio ↔ Video Audio ↔ Video Visual ↔ Transcript ↔ PPT ↔ Excel ↔ PDF ↔ Images ↔ Meeting Notes ↔ 现有相关资料。
尤其关注：人名、项目名、产品名、系统名、内部缩写、专业术语、数字、金额、百分比、时间、日期、Owner、Deadline、Status、Decision、Dependency、历史背景、当前进展。
如果 Source 之间冲突：禁止偷偷选一个版本。应该根据证据进行判断。如果可以判断：说明最可能的正确结果，并保留必要的冲突信息。如果无法可靠判断：明确标记“待确认 / Unable to confirm”，而不是编造确定答案。

## 十、会议纪要禁止套固定模板

不要按照预设的固定 PMO 模板机械生成会议纪要。不同会议可能是：项目启动会、需求讨论会、技术方案会、产品评审、项目周会、Steering Committee、Risk Review、Incident Review、业务讨论、跨团队 Alignment、Brainstorm、复盘会、数据分析会、高层决策会、普通信息同步会、其他类型会议。
不同会议的信息结构完全不同。不要提前规定最终纪要必须有哪些章节。不要因为 Prompt 中提到了某些 PM 概念，就机械生成 Decision Log、Action Items、RAID、Open Questions、Timeline、Milestones、Stakeholders、Metrics、Progress、Dependencies、Risks、Issues、Assumptions 这些内容。

## 十一、让会议本身决定纪要结构

先完整理解这场会议，再决定“对于这场会议来说，什么结构最能完整表达它？”，然后自行设计 Markdown 结构。
例如：技术方案讨论会可能重点整理当前技术问题、几套方案、每套方案原理、Trade-off、技术限制、争议、最终倾向、尚未验证的点；项目周会可能更适合当前进展、各 Workstream 状态、Blocker、变化、下一步；高层决策会可能重点是背景、决策问题、各方案、支持/反对观点、决策逻辑、最终结果、后续影响；需求讨论会可能重点是用户问题、Use Case、Requirement、Scope、Edge Case、Product Logic、Tech Constraint、Outstanding Point；复盘会可能重点是发生了什么、原因、根因、什么做对了、什么做错了、Lessons Learned、改进方向。
以上都只是示例，不要把这些示例当固定模板。最终结构必须由本场会议的信息本身决定。

## 十二、AI 必须自行判断哪些信息值得结构化

对于会议中出现的 Decision、Action、Risk、Issue、Dependency、Open Question、Timeline、Milestone、Progress、Requirement、Change、Blocker、Metric、Owner、Scope、Assumption、Trade-off、Follow-up、Technical Detail、Business Logic、Background、Context，不要因为 Prompt 提到了它们就全部强行生成独立章节。
根据信息量、重要性、会议目的、讨论深度、对理解会议的重要程度自行判断：是否需要单独整理、应该放在哪里、应该用表格还是文字、是否应该和其他内容合并、是否需要专门突出、是否根本无需单独呈现。
核心原则：结构服务于会议内容，而不是会议内容服务于模板。

## 十三、会议纪要必须“细、深、全”

最终纪要不能只是“大家讨论了 A、B、C，最后决定 X。”必须尽可能还原：为什么会讨论这个问题、问题从哪里产生、当前状态是什么、谁提出了什么、对方如何回应、为什么不同意、为什么同意、有哪些不同方案、每个方案的逻辑是什么、有什么限制、有什么前置条件、什么地方存在不确定性、哪些观点发生变化、哪些问题被解决、哪些问题没解决、什么信息只是同步、什么信息真正改变了项目、什么是会议中的重要细节、什么是上下文、最终形成了什么结果、后续意味着什么。
需要保留足够的信息密度。不要为了“看起来简洁”而把关键讨论过程压缩掉。

## 十四、理解优先于机械摘抄

会议纪要不是把 Transcript 换一种排版。应该做到：完整阅读全部材料 → 理解会议 → 理解各方逻辑 → 理解屏幕展示内容 → 结合其他资料交叉验证 → 重建会议完整语义 → 设计最合适的信息结构 → 输出详细会议纪要。
纪要应该是一份高度结构化的会议理解结果，而不是简单 Transcript Summary。

## 十五、不要过度总结

如果某个讨论持续了 20 分钟，其中包含多轮争论、三个方案、两个约束、一个技术限制、一个业务限制、两个尚未解决的问题，不能最后只写“团队讨论了方案并决定继续推进。”这种压缩属于信息损失。应该完整保留关键逻辑链。

## 十六、重要事实尽量保留 Source Traceability

对于重要信息，尽可能保留能够追溯的信息：Timestamp、Speaker、Source File、PPT Page、Excel Sheet、Screen Share Time、Document、原始材料位置。
不要求所有句子都机械加引用。但重要 Decision、关键数字、重要争议、关键时间、重要结论等，应尽可能能够回到 Source。

## 十七、完整逐字稿是强制要求

最终同一份 Markdown 文件中，除了会议纪要之外，还必须包含完整中文逐字稿。这是整个任务的核心交付之一。
逐字稿要求：尽最大能力保留会议实际说出的全部内容。不得主动：摘要、改写、润色、美化语法、删除重复、删除口头语、删除自我修正、删除插话、合并相似内容、把口语改成书面语、删除你认为“不重要”的发言。
例如原话“嗯这个，就是，我觉得我们可能还是，还是先跟 Brazil 那边确认一下，对。”不能变成“建议先与 Brazil 团队确认。”

## 十八、最终所有内容必须以中文输出

无论本次会议及输入材料是什么语言（中文、英文、葡萄牙语、西班牙语、其他语言、中英混合、多语言混合会议），最终这一份 Markdown 文件必须统一以中文为主要输出语言。
最终生成的会议纪要、完整逐字稿、投屏内容重建、PPT 内容整理、Excel / Spreadsheet 内容整理、图表说明、流程图说明、表格、File Inventory、Processing & Coverage Audit、Processing Exception、Source Conflict、所有分析说明、所有标题、所有正文、所有注释，均必须以中文输出。

## 十九、英文或其他外语会议的逐字稿必须输出为完整中文逐字译稿

如果原会议完全使用英文或其他语言，最终不要输出一份完整英文 Transcript，最终应该输出完整中文逐字译稿。
“逐字”在这里指的是保持原始会议的信息完整性、发言顺序、语义、重复、修正、插话和逻辑，而不是要求保留原始语言。
例如原始英文 “I think we should first align with the Brazil team before we lock the launch date.” 应译为“我觉得我们在最终确定上线日期之前，应该先和巴西团队对齐一下。”不能压缩成“需要先和巴西团队确认上线日期。”（后者属于摘要。）

## 二十、翻译不得造成信息压缩

例如原始英文 “Yeah, I mean, I'm not saying we can't do it. I think technically we probably can, but my concern is more about whether we actually have enough time to test the whole flow before the 24th.”
正确的完整中文逐字译稿：“对，我的意思是，我不是说我们做不了。我觉得从技术上来说我们应该是可以做的，但我更担心的是，我们在24号之前到底有没有足够的时间把整个流程完整测试一遍。”
错误：“技术上可行，但担心24号前测试时间不足。”后者只能作为会议纪要中的总结，不能代替逐字稿。

## 二十一、专业名词不要机械汉化

最终文件虽然以中文为主，但不要求消灭所有英文。以下内容如果强行翻译会影响准确性，应保留原始名称：产品名称、项目名称、系统名称、平台名称、公司名称、Team 名称、API 名称、Feature 名称、Dashboard 名称、Internal Tool 名称、技术缩写、业务缩写、指标缩写、代码、SQL、固定系统字段。
例如：SPEI、CRM、GMV、GTV、HubSpot、DIA Agent、Post Paid、Super Club、99、BCP、UAT、API。
第一次出现时，可以根据需要写成 “UAT（用户验收测试）”，后续直接使用 UAT。如果某个内部术语不存在可靠中文译法：保留原文，不要自行创造中文名称。

## 二十二、人名原则上保持原始形式

例如 Aquino、Bruno、João、James，不要为了中文化强行音译。除非现有资料中已经存在明确、稳定、可确认的中文名称。

## 二十三、中文会议中的英文表达处理

如果 Speaker 原话是“这个 dependency 我觉得还是需要先 check 一下 Brazil side，然后我们再 freeze scope。”
最终可以根据语境输出“这个 dependency（依赖）我觉得还是需要先确认一下 Brazil side（巴西侧），然后我们再 freeze scope（冻结范围）。”或者“这个依赖我觉得还是需要先确认一下巴西侧，然后我们再冻结范围。”
核心原则：中文可读性优先，但不能损失原始专业含义。

## 二十四、PPT、Excel、Dashboard 和投屏内容同样需要中文化

如果 Screen Share 中展示的是英文材料，最终重建时应尽可能转换成中文。
例如原 PPT “Launch Readiness / Current Status / Payment integration completed / UAT pending / Brazil Ops confirmation required” 最终可重建为“上线准备情况（Launch Readiness）→ 当前状态：支付集成已完成、UAT 待进行、巴西运营侧确认待完成”。
必要时可以第一次保留英文原词，但无需全文机械中英双语重复。

## 二十五、逐字稿中的视觉内容必须按时间插入

如果视频中某人在 00:24:31 打开了一张表，随后围绕这张表讨论了 8 分钟，那么逐字稿应该让未来读者知道这些人在讨论什么画面。
例如在对应时间点插入“### [开始投屏] 当前画面：[将此时屏幕中的关键内容完整结构化并转换为中文]”，然后继续逐字稿。
也就是说：Visual Context 必须与 Transcript 时间线结合。不要把所有投屏内容全部孤立扔到逐字稿之外。

## 二十六、是否需要额外整理视觉内容，由 AI 判断

如果会议投屏很多、内容复杂，则可以在同一份 Markdown 文件内部额外增加投屏内容整理、演示材料还原、数据附录、视觉内容重建等章节。如果没有必要，则不强制。由你根据本场会议的信息结构自行判断。
唯一要求：重要视觉信息不能丢。注意：即使增加这些章节，也必须全部存在于同一份最终 Markdown 文件中。禁止另建独立投屏文件。

## 二十七、会议时间和基本信息

会议日期、时间、参与人等基本信息应尽可能准确恢复。可以综合文件 Metadata、视频界面、音频、Transcript、文件名、Meeting Platform、文档、上下文、现有相关资料进行判断。如果无法可靠确定：标记“待确认”，而不是猜测。

## 二十八、最终会议纪要没有固定章节数量

最终 Markdown 可以有 5 个章节，也可以有 15 个章节，也可以大量使用 Heading、Subheading、Paragraph、Bullet、Table、Quote、Diagram、Timeline、Structured Block。完全取决于会议。
不要为了满足模板而制造没有价值的章节。也不要因为没有固定模板而丢失信息。最终判断标准不是“格式是否统一”，而是“这个结构是不是当前这场会议最合适的表达方式？”

## 二十九、最终只能输出一份文件

这是强制要求。无论会议多长、Transcript 多长、投屏内容多少，最终只允许生成一份 Markdown 文件。
这一份文件必须同时容纳：会议纪要 + 完整中文逐字稿 + 必要的视觉内容重建 + 必要的补充信息 + File Inventory + Processing & Coverage Audit + Processing Exceptions。
禁止“会议纪要.md、逐字稿.md、投屏内容.md、审计.md”这种拆分方式。也禁止“Transcript_Part_01.md、Transcript_Part_02.md”。最终必须合并成同一个 Markdown 文件。

## 三十、内容过长也不能拆文件

如果最终内容极长：不能通过拆成多个文件解决、不能通过删除内容解决、不能通过摘要 Transcript 解决、不能通过删除视觉内容解决、不能通过省略早期会议内容解决。
必须继续在同一个 Markdown 文件中完整保存。可以在同一个文件内部使用“第一部分：会议纪要 / 第二部分：完整中文逐字稿 / 第三部分：补充视觉信息 / 第四部分：处理完整性审计”，也可以根据本场会议自行设计其他内部结构。但本质始终是：一个会议 = 一份完整 Markdown 文件。

## 三十一、必须进行 Processing & Coverage Audit

虽然会议纪要正文结构自由，但文件处理完整性不能自由发挥。最终必须在同一份 Markdown 文件中，对所有输入 Source 做一次 Coverage Audit。
至少记录：文件、类型、是否完整处理、是否交叉验证、备注。
必须列出每一个文件。不能合并成“共处理 8 个文件。”我要知道具体是哪 8 个。

## 三十二、禁止虚假完成

如果没有真正打开文件、阅读文件、听完音频、看完视频、阅读全部 Sheet、阅读全部 PPT、检查全部 PDF 页面，那么绝对禁止标记为“完整处理”。

## 三十三、如果无法完整处理，必须明确报错

如果某个文件因为文件损坏、权限、Codec、加密、格式不支持、文件缺失、无法访问、音频损坏、视频损坏、内容无法解析、当前运行环境确实无法读取而没有完成：
必须在最终同一份 Markdown 文件中明确说明 Processing Exception：文件、问题、缺失内容、影响、处理状态（未完整处理）。不能偷偷跳过。

## 三十四、最终 Coverage Checklist

最终交付前必须自己检查：
- 所有输入文件均已加入 File Inventory
- 所有文件均逐一处理
- 所有音频均从第一秒处理到最后一秒
- 所有视频均从第一秒处理到最后一秒
- 所有视频均同时处理 Audio 与 Visual
- 所有独立 PPT 均逐页处理
- 所有 PDF 均逐页处理
- 所有 Excel Workbook 均完整检查
- 所有相关 Sheet 均检查
- 所有 Word / Markdown / TXT 均完整读取
- 所有图片均检查
- 所有已有 Transcript 均完整读取
- 所有 Existing Summary / Notes 均完整读取
- 原始音视频与 Transcript 已交叉校验
- 已利用现有相关资料进行必要的交叉验证
- Source Conflict 已识别
- 重要视觉内容没有遗漏
- 重要数字没有遗漏
- 重要日期没有遗漏
- 重要讨论逻辑没有被过度压缩
- 完整中文逐字稿已经生成
- 非中文会议已经完整翻译为中文逐字译稿
- 未将无法确认的信息伪装为事实
- 未将其他资料中的背景伪装成本次会议发言
- 未主动修改任何现有资料
- 未因 Token、长度或效率原因主动删除重要内容
- 所有最终输出内容均已合并到同一份 Markdown 文件
- 没有生成任何独立的第二份会议文件
- 最终文件整体以中文为主

## 三十五、推荐执行顺序

1. File Inventory
2. 完整读取所有文本 / 文档 / 表格 / 图片
3. 完整处理所有 Audio
4. 完整处理所有 Video Audio
5. 完整处理所有 Video Visual
6. 提取和重建重要 Screen Sharing 内容
7. 结合所有 Source 做 Cross-Validation
8. 使用现有相关资料进一步校验上下文、术语、人名、项目关系等
9. 理解整场会议的逻辑与目的
10. 判断本场会议最适合的信息结构
11. 编写细致完整的中文 Meeting Minutes
12. 编写完整中文逐字稿 / 完整中文逐字译稿，并在正确时间位置插入 Visual Context
13. 将所有内容合并到同一份 Markdown 文件
14. 完成 Coverage Audit
15. 检查是否存在遗漏
16. 检查最终是否只有一份文件
17. 输出最终完整 Markdown 文件

## 三十六、最终质量原则

Completeness > Brevity；Understanding > Template；Meeting-Specific Structure > Fixed Structure；Source Fidelity > Pretty Writing；Evidence > Guessing；Original Source > Existing Summary；Original Audio / Video > Auto Transcript；Cross-Validation > Single-Source Assumption；Explicit Uncertainty > Fabricated Certainty；Information Preservation > Conciseness；Chinese Final Output > Original Meeting Language；Single Complete File > Multiple Fragmented Files。
最终目标不是生成一份“长得很标准”的会议纪要。最终目标是生成一份真正完整理解了这场会议之后形成的高质量中文 Markdown 会议记录。
这一份文件应该尽可能做到：一个没有参加过会议的人能够完整看懂；一个项目负责人能够直接接着推进工作；一个 AI 能够准确理解其中所有重要上下文、关系、讨论过程和结果；即使未来无法访问原始音视频和投屏材料，也能通过这一份 Markdown 最大程度恢复整场会议。

## 三十七、最终单文件原则｜不可违反

最终交付遵循以下不可违反的规则：One Meeting = One Markdown File。
会议纪要和完整逐字稿不得拆分。中文会议纪要和完整中文逐字稿必须存在于同一份文件。投屏内容、图表、表格、视觉材料等如果需要额外整理，也必须放在这一份文件内部。Processing Audit 和 Exception 也必须放在同一份文件内部。
任何情况下都不得为了长度、Token、处理便利或结构清晰而拆成第二份文件。如果内容非常长：允许文件很长。不允许文件不完整。最终只输出这一份完整的中文 Markdown 文件。

