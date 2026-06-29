# Release Notes v0.1.0 / 发布说明 v0.1.0

## 中文

这是 `医学 OCR 识别-复核-纠错流水线 Skill` 的第一个公开版本。

本版本适用于医学教材、课件、题库截图和扫描 PDF 的 OCR 识别-复核-纠错流水线。它帮助 Codex 保留 bbox/text/confidence，检测低置信度与医学高风险 token，对局部 crop 进行二次识别，并结合医学符号规则、上下文校验和 QA 报告生成可靠输出。

### 本版本包含

- 医学 OCR 可靠性增强 pipeline skill。
- 医学 OCR 风险检测。
- 医学符号校正规则。
- 题库结构恢复。
- Mock-based 流水线验证脚本。
- Codex skill 结构校验说明。
- 中英双语 README、CHANGELOG、CONTRIBUTING 和 SECURITY 文档。

## English

This is the first public release of `Medical OCR Pipeline Skill for Codex`.

This release is intended for medical OCR refinement across textbooks, lecture slides, question-bank screenshots, and scanned PDFs. It helps Codex preserve bbox/text/confidence blocks, detect low-confidence and high-risk medical tokens, re-recognize local crops, apply medical symbol rules and context validation, and emit QA reports.

### Included

- Medical OCR refinement pipeline skill.
- Medical OCR risk detection.
- Biomedical notation correction rules.
- Question-bank structure recovery.
- Mock-based pipeline validation script.
- Codex skill validation guidance.
- Bilingual README, CHANGELOG, CONTRIBUTING, and SECURITY documentation.
