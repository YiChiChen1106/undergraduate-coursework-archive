# Skillhub 技能包说明文档

> 本项目毕业设计论文撰写专用技能包，共 **33 个 skills**，安装于 `.opencode/skills/` 目录。

---

## 一、学术写作（Academic Writing）

### 1. academic-writing
**版本：** 1.0.0
学术写作技能，覆盖论文、文献综述、研究方法及论文构词，遵循严格的学术标准和引用规范。

### 2. academic-writing-refiner
**版本：** 1.0.0
为计算机科学顶会论文（NeurIPS、ICLR、ICML、AAAI、IJCAI、ACL、EMNLP、NAACL、CVPR、WWW、KDD、SIGIR、CIKM 等）提供精修润色服务，支持全文精修和分节编辑，涵盖摘要、引言、相关工作、方法论、实验、结论等全部章节。也适用于"LaTeX内容润色"、"camera-ready"、"rebuttal"、"paper revision"等场景。

### 3. academic-writing-assistant
**版本：** 1.0.0
学术写作辅助技能，提供段落撰写、语言润色、语法检查、学术风格优化及引用格式检查。

### 4. academic-writer
**版本：** 0.1.0
专业 LaTeX 写作助手，功能包括：扫描现有 LaTeX 模板、读取参考材料（Word/文本）、严格按模板起草内容、编译 PDF。触发关键词：'write thesis'、'draft section'、'compile pdf'、'check latex format'。与 'academic-research-hub' 协同获取引用。

### 5. research-paper-writer
**版本：** 0.1.0
遵循 IEEE/ACM 格式标准创建正式学术论文，包含规范的结构、引用和学术写作风格。用于撰写任何主题的研究论文、学士论文或学术论文。

### 6. paper-writing-workflow
**版本：** 1.0.0
标准化论文写作流程，整合 academic-writing、research-paper-writer、scientific-writing 等技能，提供完整的论文写作流程，涵盖从选题到最终稿件的 6 个阶段。

### 7. paper-assistant
**版本：** 1.0.0
面向论文选题、提纲、摘要、引言、文献综述、研究方法、结果讨论、润色改写与投稿准备的论文助手。

### 8. paper-check
**版本：** 1.0.0
本科/研究生毕业论文格式规范检测、自动修复与对比报告生成工具。支持任意学校的撰写规范文档（.doc/.docx/.txt/.pdf）输入，自动解析规范要求并与论文文档逐项对比检测。触发场景："论文格式检查"、"毕业论文排版"、"格式规范检测"、"论文格式修复"、"对比报告"。

### 9. harvard-paper-zh
**版本：** 0.1.0
将中文需求快速改写并排版为哈佛格式论文（含摘要、关键词、目录、分级标题、参考文献），并导出 .docx。用户提到"写论文"、"哈佛格式"、"学术润色"、"生成Word论文"、"参考文献Harvard"时使用。

---

## 二、文献与研究（Literature & Research）

### 10. literature-review
**版本：** 1.2.0
通过 Semantic Scholar、OpenAlex、Crossref 和 PubMed API 搜索学术文献，协助撰写文献综述。用于用户需要按主题查找论文、获取特定 DOI 详情或起草带正确引用的文献综述章节。

### 11. literature-search
**版本：** 1.0.3
在 Google Scholar、PubMed、arXiv、IEEE、ACM、Semantic Scholar、Scopus 和 Web of Science 上查找并汇编学术文献及引用列表。用于"find related literature"、"related work"、"citation list"、"key papers on a topic"等请求。

### 12. academic-search
**版本：** 1.0.0
在 arXiv、Google Scholar 和 Semantic Scholar 上进行系统性搜索，找到并分析、总结 Top 5 相关学术论文的摘要内容。

### 13. academic-research-hub
**版本：** 0.1.0
用于搜索学术论文、下载研究文档、提取引用及收集学术信息。触发关键词："find papers on"、"search research about"、"download academic articles"、"get citations for"，或涉及 arXiv、PubMed、Semantic Scholar、Google Scholar 等数据库。也适用于文献综述、参考文献生成和研究发现。

### 14. academic-researcher
**版本：** 1.0.0
学术研究助手，面向文献综述、论文分析和学术写作。用于：审阅学术论文、进行文献综述、分析研究方法、格式化引用或学术论文撰写。

### 15. academic-deep-research
**版本：** 1.0.0
透明、严格的研究方法，非黑盒 API 封装。通过每主题强制 2 轮研究、APA 第7版引用、证据层级和 3 个用户检查点进行详尽调查。使用原生 OpenClaw 工具（web_search、web_fetch、sessions_spawn）。适用于文献综述、竞争情报或任何需要学术严谨性和可重复性的研究。

### 16. paper-recommendation
**版本：** 1.0.1
自动化发现、并行审阅、评分和 AI 研究论文简报生成（来自 arXiv），支持每日更新和 PDF 分析。

### 17. paper-parse
**版本：** 1.0.0
对用户提供的任何学术论文（PDF附件或URL）进行双模式深度研读。一次性生成两份报告：Part A 面向研究者的深度专业解析，Part B 面向快速理解的核心逻辑与价值提炼。

### 18. paper-fetcher
**版本：** 1.0.0
根据 DOI 从 Sci-Hub 获取学术论文。自动下载 PDF 并以干净文件名保存到 research/papers/ 目录。用户提供 DOI 或请求 PubMed 论文时使用。

### 19. zotero
**版本：** 1.0.0
通过 Web API 管理 Zotero 参考书库。功能包括：搜索、列出项目，通过 DOI/ISBN/PMID 添加项目（含重复检测），删除/回收站项目，更新元数据和标签，导出 BibTeX/RIS/CSL-JSON，批量从文件添加，检查 PDF 附件，跨引用引用，通过 CrossRef 查找缺失 DOI，获取开放获取 PDF。支持 --json 输出用于脚本编写。用户询问学术参考、引用管理、文献库、论文 PDF、参考文献导出或 Zotero 时使用。

---

## 三、图表与可视化（Diagrams & Visualization）

### 20. mermaid-architect
**版本：** 1.0.0
生成精美、手绘风格的 Mermaid 图表，支持健壮语法（引号标签、ELK 布局）。当用户请求"diagram"、"flowchart"、"sequence diagram"或"visualize this process"时使用。

### 21. drawio
**版本：** 1.0.0
生成专业 draw.io 图表（ERD/数据库表、类图、序列图、流程图、架构图）并导出为 PNG。当用户请求任何图表、数据库模型、类结构、流程或系统可视化时使用。

### 22. diagram-generator
**版本：** 1.1.1
生成并编辑多种类型的图表，支持 drawio、mermaid、excalidraw 格式。支持：系统架构图、时序图、流程图、ER 图、思维导图、架构图、网络拓扑图等多种常见图表类型。可通过自然语言生成图表，也可读取并修改现有的 drawio/mermaid/excalidraw 文件。支持自动创建子目录，默认路径为项目目录下的 `diagrams/{format}/`。

### 23. excalidraw-diagram-generator
**版本：** 1.0.0
根据自然语言描述生成 Excalidraw 图表。当用户要求"create a diagram"、"make a flowchart"、"visualize a process"、"draw a system architecture"、"create a mind map"或"generate an Excalidraw file"时使用。支持流程图、关系图、思维导图和系统架构图。

### 24. chart-image
**版本：** 2.6.18
从数据生成出版质量的图表图像。支持折线图、柱状图、面积图、点图、K线图、饼图/甜甜圈图、热力图、多系列图和堆叠图。用于可视化数据、创建图表、绘制时间序列或生成报告/警报图表图像。专为 Fly.io/VPS 部署设计，无需本地编译、Puppeteer 或浏览器，纯 Node.js 和预编译二进制文件。

### 25. presentation-agent
**版本：** 1.0.0
使用 Marp 将 Markdown 文档转换为演示文稿（PDF/PPTX/HTML）。支持 Mermaid 图表（甘特图、流程图等）和数据图形。当用户要求创建幻灯片、演示文稿或 deck 时使用。

---

## 四、公式与格式（Formula & Format）

### 26. academic-formula-converter
**版本：** 1.0.0
将 Markdown 中的 LaTeX 数学公式转换为支持 Unicode 符号的精美 docx 或 HTML 文档，用于学术用途。

### 27. paper-engineering-assistant
**版本：** 1.0.1
基于"采集-整理-撰写"三层架构的自动化论文写作助手。按照用户指定的项目目录（`workspace/毕业设计`）结构化组织所有文件。

---

## 五、答辩辅助（Defense & Review）

### 28. academic-discussion-assistant
**版本：** 1.0.1
当用户要进行研究生组会、与导师讨论论文修改、技术方案推敲等小规模学术讨论录音转成纪要，并提取老师意见、学生回应、待修改事项和后续动作时触发。适用于 2~3 人、以老师和学生为主的学术讨论场景。Skill 优先使用 SenseAudio ASR 的说话人分离能力，再结合 Agent 的大模型摘要能力，最后调用 SenseAudio TTS 返回适合收听的语音摘要。

### 29. academic-pre-review-committee
**版本：** 1.0.0
由五位资深审稿人组成的"学术预审委员会"，根据用户需求调度对应审稿人角色进行论文审查。支持全面审稿（依次调度全部五个角色）和指定维度审稿。触发关键词：审稿、预审、论文审查、理论贡献、方法论、文献对话、逻辑链条、主编预筛、desk reject。

### 30. academic-mentor
**版本：** 1.0.0
AI 驱动的研究生科研导师——提供研究评估、提案生成、文献分析、导师匹配和发表指导。

---

## 六、通用写作（General Writing）

### 31. writing
**版本：** 1.1.0
适配写作风格，提高清晰度，跨会话记忆写作偏好。

### 32. writing-polish
**版本：** 1.0.0
中文写作润色。当用户要求润色文章、改写段落、优化文风、修改措辞、让文章更通顺、写作辅助、改稿、polish writing，或者给出一段中文文本要求改善时使用此 skill。也适用于用户说"帮我改改这篇文章"、"润色一下"、"语言不够好"、"读起来不顺"、"太空洞了"、"太说教了"等场景。

### 33. humanizer
**版本：** 1.0.0
去除文本中 AI 生成写作的痕迹，使文章听起来更自然、更像人类写作。基于维基百科全面的"AI 写作迹象"指南。检测并修复的模式包括：膨胀的象征主义、促销语言、肤浅的-ing 分析、模糊归属、破折号过度使用、三法则、AI 词汇、负面平行结构和过多连词短语。

---

## 七、技能索引

| 编号 | 名称 | 版本 | 类别 |
|------|------|------|------|
| 1 | academic-writing | 1.0.0 | 学术写作 |
| 2 | academic-writing-refiner | 1.0.0 | 学术写作 |
| 3 | academic-writing-assistant | 1.0.0 | 学术写作 |
| 4 | academic-writer | 0.1.0 | 学术写作 |
| 5 | research-paper-writer | 0.1.0 | 学术写作 |
| 6 | paper-writing-workflow | 1.0.0 | 学术写作 |
| 7 | paper-assistant | 1.0.0 | 学术写作 |
| 8 | paper-check | 1.0.0 | 格式检查 |
| 9 | harvard-paper-zh | 0.1.0 | 学术写作 |
| 10 | literature-review | 1.2.0 | 文献研究 |
| 11 | literature-search | 1.0.3 | 文献研究 |
| 12 | academic-search | 1.0.0 | 文献研究 |
| 13 | academic-research-hub | 0.1.0 | 文献研究 |
| 14 | academic-researcher | 1.0.0 | 文献研究 |
| 15 | academic-deep-research | 1.0.0 | 文献研究 |
| 16 | paper-recommendation | 1.0.1 | 文献研究 |
| 17 | paper-parse | 1.0.0 | 文献研究 |
| 18 | paper-fetcher | 1.0.0 | 文献研究 |
| 19 | zotero | 1.0.0 | 文献研究 |
| 20 | mermaid-architect | 1.0.0 | 图表绘制 |
| 21 | drawio | 1.0.0 | 图表绘制 |
| 22 | diagram-generator | 1.1.1 | 图表绘制 |
| 23 | excalidraw-diagram-generator | 1.0.0 | 图表绘制 |
| 24 | chart-image | 2.6.18 | 图表绘制 |
| 25 | presentation-agent | 1.0.0 | 图表绘制 |
| 26 | academic-formula-converter | 1.0.0 | 公式格式 |
| 27 | paper-engineering-assistant | 1.0.1 | 公式格式 |
| 28 | academic-discussion-assistant | 1.0.1 | 答辩辅助 |
| 29 | academic-pre-review-committee | 1.0.0 | 答辩辅助 |
| 30 | academic-mentor | 1.0.0 | 答辩辅助 |
| 31 | writing | 1.1.0 | 通用写作 |
| 32 | writing-polish | 1.0.0 | 通用写作 |
| 33 | humanizer | 1.0.0 | 通用写作 |

---

## 八、使用场景快速查询

| 场景 | 推荐技能 |
|------|---------|
| 写论文正文各章节 | `academic-writing` → `academic-writing-refiner` |
| 生成 IEEE/ACM 格式论文 | `research-paper-writer` |
| 完整论文写作流程 | `paper-writing-workflow` |
| LaTeX 论文 + PDF 编译 | `academic-writer` |
| 文献综述构建 | `literature-review` + `zotero` |
| 搜索相关论文 | `academic-search` / `literature-search` |
| 获取论文 PDF | `paper-fetcher` |
| 论文格式检查与修复 | `paper-check` |
| 系统架构图 | `mermaid-architect` / `drawio` |
| 实验数据图表 | `chart-image` |
| 答辩 PPT | `presentation-agent` |
| 论文公式转 docx | `academic-formula-converter` |
| 中文润色 | `writing-polish` |
| 去 AI 写作痕迹 | `humanizer` |
| 答辩 Q&A 准备 | `academic-pre-review-committee` |
| 答辩材料整理 | `academic-discussion-assistant` |

---

*文档生成时间：2026-04-10*
*技能包来源：skillhub.cn*
