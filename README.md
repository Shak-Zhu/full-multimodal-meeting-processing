# Full Multimodal Meeting Processing

一个会议交付一份中文 Markdown 的全量多模态会议处理技能，包含：

- 深度会议纪要
- 完整中文逐字稿 / 逐字译稿
- 按时间插入的投屏与视觉上下文
- 文件处理完整性审计、异常与来源冲突记录

## 文件结构

- `SKILL.md`：技能入口与执行流程
- `references/constitution.md`：完整处理宪法
- `references/lessons-learned.md`：历史踩坑与质量要求
- `scripts/inventory.py`：文件清单生成器
- `scripts/verbatim.py`：逐字稿骨架生成器
- `agents/openai.yaml`：Codex 技能展示配置
- `dependencies/tencent-meeting-extract/`：腾讯会议录制提取技能及下载脚本，处理腾讯会议链接时随包使用

## 使用

将本仓库目录放入 Codex 技能目录，并按 `SKILL.md` 中的规则调用。

腾讯会议录制链接场景所需的提取技能和下载脚本已随仓库提供，无需依赖本机其他技能目录。

