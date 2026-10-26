# Word 生成与核验

## 选择格式依据

新建意见使用随 skill 保存的模板和生成脚本。用户提供并指定当前 DOCX 时，在其副本上局部改字，保留标题、字体、段落、编号、页边距和显式分页等原有设置；不要用默认模板重建。再次编辑前核对文件当前正文，避免覆盖用户在上次交付后的修改。中英文保持条目和含义对应，不通过缩字或强制断页追求相同页数。

## 数据准备

使用 workspace dependency loader 返回的 Python 及其 `lxml`。所有路径从当前 `SKILL.md` 所在文件夹解析，不假定 skill 位于工作目录。

在任务临时目录写一个 UTF-8 JSON：

```json
{
  "manuscript_id": "THE-ACTUAL-MANUSCRIPT-ID",
  "language": "en",
  "summary": "The complete, evidence-based overall assessment in one paragraph.",
  "comments": [
    "The first complete comment without a manually typed number.",
    "The second complete comment without a manually typed number."
  ]
}
```

`language` 为 `en` 或 `zh`；它决定模板，不会自动翻译内容。`summary` 和每条 comment 必须为单段文本。`comments` 可为空，例如有依据的直接接收，不为满足默认条数编造问题。不要将审核笔记写进 JSON 的正文。

## 生成

按当前 documents skill 完成一次必要的文档创建登记，然后运行：

```powershell
& $PythonBin "$SkillDir/scripts/build_review_docx.py" `
  --input "$TaskTemp/review.json" `
  --output "$OutputDir/Review for THE-ACTUAL-MANUSCRIPT-ID.docx"
```

脚本从 `assets/review-en.docx` 或 `assets/review-zh.docx` 克隆角色段落，沿用包内样式、编号及页面设置。它只替换正文和文档标题元数据，所有其他成员保持逐字节不变。输入非法、输出已存在或输出会覆盖输入/模板时失败；选择新文件名后重跑，不静默覆盖原论文或旧审稿记录。

脚本支持纯文字、Unicode 希腊字母和上下标字符，不将 LaTeX/Markdown 自动转换为 Word 公式。需要复杂公式、富文本或原记录的多段子问题时，用 documents 工具在输出副本中局部编辑，保持格式规则，并重新核验。

## 核验

1. 脚本自动重新打开输出：核对标题、总评和所有意见文字；核对自动编号使用的 numId/ilvl；核对 `sectPr` 及所有不应改动的 ZIP 成员。
2. 用 documents 的 `render_docx.py` 渲染全部页并检查图片。当前 Windows 环境如缺少 LibreOffice，可使用本机 Word 的只读 `ExportAsFixedFormat` 导出临时 PDF，再以 Poppler 转 PNG；不要通过另存原文件改变模板或源稿。
3. 按选定模板或用户现稿核对标题、字体、编号、缩进、对齐、换页和希腊字母/上下标，避免文字裁切、漏字、孤立编号或异常空白页。内容变长可以自然跨页，不能为强行一页而缩小字体。
4. 校对渲染后的文字和最终确定的评论内容一致。没有完成页面检查就不声称视觉验证通过。

原模板来源和样式依据见 `style-and-format.md`、`history-and-examples.md`、`template-provenance.json`。生成的 JSON、PDF 和 PNG 为任务内核验材料，默认只交付最终 DOCX。
