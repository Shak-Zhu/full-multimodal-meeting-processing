# Full Multimodal Meeting Processing

全量多模态会议处理 Skill：一个会议交付一份中文 Markdown，含深度纪要、完整中文逐字稿或逐字译稿、视觉重建、完整性审计及异常与冲突记录。

## 分享与下载

公开仓库：https://github.com/Shak-Zhu/full-multimodal-meeting-processing

- [完整 ZIP 下载](https://github.com/Shak-Zhu/full-multimodal-meeting-processing/archive/refs/heads/main.zip)，无需 GitHub 登录。
- 克隆：`git clone https://github.com/Shak-Zhu/full-multimodal-meeting-processing.git`
- 固定版本：克隆后 `git checkout <完整提交 SHA>`，避免 main 后续变化影响复现。

必须下载整个仓库，仅复制 SKILL.md 会丢失宪法、经验教训和脚本。仓库无 submodule、LFS 或指向作者本机的软链接，腾讯会议提取依赖已随包提供。

## 安装与调用

使用默认技能目录的 Codex 可将仓库放为 `~/.codex/skills/full-multimodal-meeting-processing`；自定义目录则使用实际路径。已有同名安装时先比较、备份，不直接覆盖。按客户端技能加载机制刷新或重启，再使用 `$full-multimodal-meeting-processing`。

其他具备本地文件读取和工具执行能力的 Agent 可下载到独立目录，从 [SKILL.md](SKILL.md) 开始阅读。自动注册和工具接口因客户端而异。可将下面这段直接分享给其他 Agent：

> 请完整下载 https://github.com/Shak-Zhu/full-multimodal-meeting-processing ，保留所有子目录。阅读 README.md、SKILL.md、references/constitution.md 和 references/lessons-learned.md，检查运行前提并核验 SHA256SUMS。处理我提供的会议材料时遵循该 Skill；工具或资料不可用时如实记录异常，不得声称已完整处理。

## 运行前提

仓库包含完整技能文本和辅助脚本。以下运行能力需要接收方准备；模型、会议原始材料、账号权限与作者知识库不随包分发。

| 场景 | 需要的能力或依赖 |
|---|---|
| 脚本、包校验及离线测试 | Python 3.9 或更高版本；辅助脚本使用标准库 |
| 音视频时长、音轨、抽帧 | ffmpeg、ffprobe；afinfo 仅为 macOS 可选回退 |
| 独立全长 ASR | whisper-cli + 模型，或可用的 faster-whisper / mlx-whisper 及模型；记录实际引擎、参数和覆盖范围 |
| DOCX / XLSX / PPTX | 如 python-docx、openpyxl、python-pptx 等解析器；textutil 仅为 macOS 可选工具 |
| PDF、图片、投屏 | PDF 逐页解析/渲染，以及 Agent 的图像理解能力；仅 OCR 不能证明结构还原完整 |
| 腾讯会议录制 | curl、ffprobe、有效访问权限，必要时使用已登录浏览器；内置脚本不能绕过权限或过期签名 |
| 历史资料交叉验证 | 用户提供或授权访问的资料；无法访问须说明缺口 |
| 长会议 | 足够存储、持续执行能力和可追溯的断点恢复 |

按实际输入准备依赖。下载成功不等于具备全量会议处理能力。原作者的 M4 Pro 性能、代理、模型缓存与浏览器 API 是历史个案，其他环境须重新确认。Chat 改名工具不可用时按 SKILL.md 给出建议标题。

## 内容与核验

- [SKILL.md](SKILL.md)：入口、流程和边界。
- [宪法](references/constitution.md)：37 条用户原文。
- [经验教训](references/lessons-learned.md)：12 节历史踩坑与质量要求。
- [清单脚本](scripts/inventory.py)：隐藏项会提示，可用 `--include-hidden` 纳入；符号链接目录等未遍历内容仍须人工核对。
- [逐字稿脚本](scripts/verbatim.py)：TicNote 骨架，不替代 ASR、翻译或身份核验。
- [展示配置](agents/openai.yaml)。
- [腾讯会议提取依赖](dependencies/tencent-meeting-extract/SKILL.md) 与 [下载脚本](dependencies/tencent-meeting-extract/scripts/tm_download.py)。
- [离线回归测试](tests/test_helpers.py)、[校验脚本](scripts/verify_package.py)、[SHA256SUMS](SHA256SUMS)。
- [分享核验记录](references/distribution-audit.md)：经验教训对照、验证范围和局限。

下载后在仓库目录运行：

```bash
python3 scripts/verify_package.py
python3 -m unittest discover -s tests -v
```

校验脚本逐文件比对 SHA-256，缺失或改动时以非零状态退出。清单覆盖发布文件（自身除外），用于一致性校验，不替代来源身份验证。离线测试不访问真实会议，不证明 ASR、视觉理解或身份裁定已经完成。
