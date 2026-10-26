# Review Paper Comments

用于审阅论文并生成中英文 referee comments 的 Codex skill，重点关注物理机制、模型假设、创新性、数值可靠性和定量验证。

默认输出沿用简洁的审稿格式：

```text
Comments on <manuscript identifier>

一段总评：研究对象与方法、贡献、主要不足及发表判断。

1. 原文依据、具体问题及其影响，以及作者需要回答的问题。
2. 下一条有原文依据的意见。
```

支持同格式 Word 输出：A4、Times New Roman/宋体 12 pt、居中加粗标题、两端对齐正文和连续自动编号。中文模板保留总评首行缩进及条目间空行。

## 使用

将本仓库的 skill 文件放入个人 skills 目录下的 `review-paper-comments` 文件夹，保留 `SKILL.md`、`agents`、`references`、`scripts` 和 `assets` 的相对位置。Git 元数据无需放入 skills 目录。

提供论文后调用：

```text
$review-paper-comments 审阅这篇论文，按既往格式输出 comments 和 Word。
```

英文论文默认输出英文，中文论文默认输出中文；也可明确指定语言。仅有摘要时，只给限定范围的初步意见。判断和建议须依据当前论文，不套用历史稿件的具体批评。

意见默认以关键科学问题为主，让作者选择解决方法；仅在影响核心结论时讨论计算实现细节。交付前对照原文核对术语、物理量定义和语气，并同步中英文表述。修改用户指定的现稿时沿用其最新格式。

## Word 生成

审阅完成后，将稿件标识、语言、总评和意见列表写入 JSON，再运行：

```bash
python scripts/build_review_docx.py --input review.json --output "Review for MANUSCRIPT-ID.docx"
```

脚本需要 Python 和 `lxml`；在 Codex 中使用工作区依赖工具提供的运行环境。JSON 格式、排版和视觉核验步骤见 [Word 生成与核验](references/docx-output.md)。

脚本会检查输出文字、编号、页面设置和未修改的文档包成员，并拒绝覆盖已有文件。生成后仍需渲染检查页面。

## 文件

- [SKILL.md](SKILL.md)：审阅流程和交付要求。
- [references](references/)：写作风格、技术审阅标准、匿名示例和 Word 使用说明。
- [assets](assets/)：清除旧正文和作者元数据的中英文 Word 模板。
- [scripts/build_review_docx.py](scripts/build_review_docx.py)：保持模板排版的生成工具。

本公开版本从历史审稿记录提炼通用规则，使用重新编写的匿名示例；不包含原始论文、历史审稿全文、真实稿件编号或本机文件路径。Word 模板和中英文回填结果已通过结构校验及逐页检查。
