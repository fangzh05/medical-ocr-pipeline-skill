# 医学教材OCRskills / Medical Textbook OCR Skills

## 中文说明

这是一个用于 Codex 的医学教材 OCR 技能包，适合处理医学截图、扫描版 PDF、教材页面、课件幻灯片、题库图片和混合排版文档。

它的目标不只是“识别文字”，而是尽量保留医学学习资料中容易被普通 OCR 破坏的结构和符号，包括：

- 医学生物医学符号和上下标
- 化学式、离子、电解质和酸碱平衡符号
- 呼吸、血气、肺功能等生理参数
- 表格结构
- 公式区域
- 题库题干、选项、答案和解析
- Markdown 结构化输出

例如，普通 OCR 可能把 `PaCO₂`、`HCO₃⁻`、`SpO₂`、`FEV₁/FVC`、`HbA₁c` 识别成 `PaCO2`、`HCO3-`、`SpO2`、`FEV1/FVC`、`HbA1c`。这个 skill 会提示 Codex 使用更合适的 OCR 路由，并在识别后执行医学符号校正和质量检查。

## English

This is a Codex skill package for high-fidelity OCR of medical textbooks, screenshots, scanned PDFs, lecture slides, question-bank images, and mixed-layout documents.

Its goal is not only to extract text, but also to preserve layout-sensitive and meaning-sensitive medical content, including:

- biomedical notation with subscripts and superscripts
- chemical formulas, ions, electrolytes, and acid-base notation
- respiratory, blood gas, pulmonary function, and physiology parameters
- table structure
- formula regions
- question stems, choices, answers, and explanations
- structured Markdown output

For example, plain OCR may flatten `PaCO₂`, `HCO₃⁻`, `SpO₂`, `FEV₁/FVC`, and `HbA₁c` into `PaCO2`, `HCO3-`, `SpO2`, `FEV1/FVC`, and `HbA1c`. This skill guides Codex to route OCR more carefully, then apply biomedical notation correction and quality checks.

## 仓库结构 / Repository Layout

```text
skills/
  medical-ocr-router/
    SKILL.md
    agents/openai.yaml
    references/
      biomedical-notation.md
      ocr-routing.md
    scripts/
      medical_corrector.py
      test_medical_corrector.py
```

## 安装 / Install

```powershell
python C:\Users\16648\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --url https://github.com/fangzh05/medical-ocr-router-skill/tree/main/skills/medical-ocr-router
```

安装后重启 Codex。  
Restart Codex after installation.

## 本地验证 / Local Validation

```powershell
python skills\medical-ocr-router\scripts\test_medical_corrector.py
python C:\Users\16648\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\medical-ocr-router
```

## 适用场景 / Use Cases

- 医学教材扫描件 OCR / OCR scanned medical textbook pages
- 中文医学课件转 Markdown / Convert Chinese medical slides to Markdown
- 医学题库截图识别 / Extract question-bank screenshots
- 血气、电解质、甲功、肺功能等符号校正 / Correct ABG, electrolyte, thyroid, and pulmonary notation
- 表格、公式、混合排版页面的结构保留 / Preserve tables, formulas, and mixed document layout

