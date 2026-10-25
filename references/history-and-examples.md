# 匿名来源与写法示例

本 skill 从 8 份个人审稿记录提炼，保留总评与编号意见的结构，以及物理机制、假设检验和定量验证等关注点。原始记录不随公开版本分发。

## 已观察到的写作习惯

- 以一段总评介绍研究、具体贡献与发表倾向，再列编号意见。
- 8 份记录共 32 条主要意见，单份为 3–6 条，多数为 4 条。该范围仅用于把握密度。
- 科学问题在前，确实存在的单位、符号或图注问题在后；没有小问题时不强行添加。
- 英文与中文正文分别跟随稿件语言，标题统一为 `Comments on ...`。
- 将问题、影响和合理补充连成段落，避免只有泛泛的批评。

## 重新编写的示例

以下内容是说明写法的虚构示例，不是历史审稿原文，也不构成对任何论文的判断。只有新论文中存在对应证据时，才可使用相应论证结构。

**假设与适用条件**

The statistical formulation treats the two fitted parameters as independent. The manuscript should explain whether this assumption was checked against the available samples and whether plausible dependence would alter the predicted response. A sensitivity analysis would help establish the range over which the approximation is reliable.

**同一过程的两种分析方法**

The analytical estimate and the numerical calculation appear to describe the same transition, but they use different loading conditions. Please clarify whether their results can be compared directly. A comparison under matched conditions would make the physical interpretation easier to assess.

**定性一致与定量验证**

文中的对照主要展示了变化趋势的一致性，尚不清楚模型对关键观测量的预测误差。建议在可比工况下报告代表性量的定量偏差，并说明边界条件或参数标定可能造成的差异，以明确验证的强度和适用范围。

**缺少说明与证据不足的区别**

The current description does not explain how the damage evolution contributes to the energy balance. Please provide the relevant formulation or a representative energy history so that the treatment of dissipation can be assessed. This request concerns an unreported check; it does not, by itself, establish that the method is inconsistent.

**发表判断**

对已有充分支持的核心结论，可提出局部修订；对影响核心解释但可修复的缺口，应明确实质修订要求。拒稿结论需对应有证据的贡献或可靠性问题，不应仅由意见数量或格式问题决定。

## 模板来源与公开范围

中英文 Word 模板各从一份代表性记录复制排版，正文已替换成可填充标记，文档作者及自定义元数据已清除。公开版本不包含原始稿件、稿件编号、原审稿摘录、来源文件路径或原始文件哈希。

模板本身的校验值见 [template-provenance.json](template-provenance.json)。英文模板保留连续条目，中文模板保留总评首行缩进及条目间空行。可在缺少历史原件的环境中直接使用这些模板。
