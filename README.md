# 医学教材OCRskills / Medical Textbook OCR Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](RELEASE_NOTES_v0.1.0.md)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827.svg)](skills/medical-ocr-router/SKILL.md)

医学教材 OCR 路由与医学符号校正 Codex Skill。  
Medical textbook OCR routing and biomedical notation correction skill for Codex.

## 中文说明

这是一个用于 Codex 的医学教材 OCR 技能包，适合处理医学截图、扫描版 PDF、教材页面、课件幻灯片、题库图片和混合排版文档。

它的目标不只是“识别文字”，而是尽量保留医学学习资料中容易被普通 OCR 破坏的结构和符号。普通 OCR 可能把 `PaCO₂`、`HCO₃⁻`、`SpO₂`、`FEV₁/FVC`、`HbA₁c` 识别成 `PaCO2`、`HCO3-`、`SpO2`、`FEV1/FVC`、`HbA1c`。这个 skill 会提示 Codex 使用更合适的 OCR 路由，并在识别后执行医学符号校正和质量检查。

## English

This is a Codex skill package for high-fidelity OCR of medical textbooks, screenshots, scanned PDFs, lecture slides, question-bank images, and mixed-layout documents.

Its goal is not only to extract text, but also to preserve layout-sensitive and meaning-sensitive medical content. Plain OCR may flatten `PaCO₂`, `HCO₃⁻`, `SpO₂`, `FEV₁/FVC`, and `HbA₁c` into `PaCO2`, `HCO3-`, `SpO2`, `FEV1/FVC`, and `HbA1c`. This skill guides Codex to route OCR more carefully, then apply biomedical notation correction and quality checks.

## 功能特点 / Features

- 医学 OCR 路由：根据文本、公式、表格、混合版面和题库页面选择合适处理路径。
- 医学符号校正：修复常见 OCR 扁平化结果，如 `PaCO2` -> `PaCO₂`、`HCO3-` -> `HCO₃⁻`。
- 表格和公式保护：提示 Codex 避免把表格、公式和上下标结构压平成普通文本。
- 题库结构保留：保留题号、题干、选项、答案和解析的分区。
- Markdown 输出：面向医学学习、教材整理和题库复习生成结构化 Markdown。
- 本地验证脚本：提供医学符号校正 smoke test 和 Codex skill 格式校验。

- Medical OCR routing: choose suitable processing paths for text, formulas, tables, mixed layouts, and question-bank pages.
- Biomedical notation correction: repair common flattened OCR output such as `PaCO2` -> `PaCO₂` and `HCO3-` -> `HCO₃⁻`.
- Table and formula preservation: guide Codex not to flatten structure-sensitive content.
- Question-bank structure preservation: keep question number, stem, options, answer, and explanation separated.
- Markdown output: generate structured Markdown for medical study, textbook reconstruction, and exam review.
- Local validation scripts: include a biomedical notation smoke test and Codex skill validation.

## 仓库结构 / Repository Layout

```text
medical-ocr-router-skill/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── RELEASE_NOTES_v0.1.0.md
├── .gitignore
└── skills/
    └── medical-ocr-router/
        ├── SKILL.md
        ├── agents/
        ├── references/
        └── scripts/
```

## 安装 / Installation

使用 Codex 自带的 skill installer 安装：

```powershell
python C:\Users\16648\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --url https://github.com/fangzh05/medical-ocr-router-skill/tree/main/skills/medical-ocr-router
```

安装后重启 Codex。  
Restart Codex after installation.

## 使用方式 / Usage

在 Codex 中处理医学 OCR 任务时，可以直接提出类似请求：

```text
Use $medical-ocr-router to OCR this medical textbook screenshot into Markdown and preserve biomedical notation.
```

也可以用中文描述：

```text
请用 $medical-ocr-router 识别这张医学教材截图，保留表格、公式和 PaCO₂、HCO₃⁻ 这类医学符号。
```

该 skill 会引导 Codex 在普通 OCR、公式识别、表格识别、版面分析和医学符号校正之间进行路由。

## 验证 / Validation

提交修改前建议运行：

```powershell
python skills\medical-ocr-router\scripts\test_medical_corrector.py
python C:\Users\16648\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\medical-ocr-router
```

第一条命令验证医学符号校正规则。第二条命令验证 Codex skill 元数据和结构。

## 局限性 / Limitations

- 本仓库提供 Codex skill 指南和后处理脚本，不内置完整 OCR 引擎。
- 公式识别、表格识别和版面分析能力取决于本地环境中可用的 OCR 工具。
- 医学符号校正是保守规则，不能替代人工校对。
- 对真实病历、检查报告或患者资料进行 OCR 前，必须先脱敏。

- This repository provides a Codex skill guide and post-processing scripts, not a full OCR engine.
- Formula, table, and layout recognition depend on the OCR tools available in the local environment.
- Biomedical notation correction is conservative and does not replace human review.
- Real clinical records, reports, or patient materials must be de-identified before OCR.

## 隐私提醒 / Privacy Notice

不要上传患者隐私、真实病历、身份证号、手机号、医院号、检查报告原图或其他敏感信息。公开 issue、PR 和示例文件中只能使用脱敏样例或合成数据。

Do not upload patient privacy data, real medical records, ID numbers, phone numbers, hospital IDs, original examination report images, or other sensitive information. Public issues, pull requests, and examples should use only de-identified samples or synthetic data.

## 后续计划 / Roadmap

- 增加更多医学符号校正规则。
- 补充更多中文医学教材和题库 OCR 示例。
- 增加可选 OCR pipeline 示例。
- 改进表格和公式区域的复核提示。
- Add more biomedical notation correction rules.
- Add more Chinese medical textbook and question-bank OCR examples.
- Add optional OCR pipeline examples.
- Improve review hints for table and formula regions.

## 开源协议 / License

本项目使用 MIT License。详见 [LICENSE](LICENSE)。  
This project is licensed under the MIT License. See [LICENSE](LICENSE).

