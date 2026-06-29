# 医学 OCR 后处理与质量控制 Codex Skill / Medical OCR Corrector & QA Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](RELEASE_NOTES_v0.1.0.md)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827.svg)](skills/medical-ocr-router/SKILL.md)

面向医学教材、课件、题库、扫描 PDF 和截图 OCR 文本的后处理与质量控制 Codex Skill。  
A Codex skill for post-processing and quality-checking OCR text from medical textbooks, slides, question banks, scanned PDFs, and screenshots.

## 中文说明

这个项目的重点不是选择 OCR 工具，而是在 OCR 之后把医学文本整理到可学习、可复核、可发布的状态。

它会引导 Codex 对医学 OCR 文本进行：

- 医学符号纠错：如 `PaCO2` -> `PaCO₂`、`HCO3-` -> `HCO₃⁻`
- 题库结构恢复：题号、题干、选项、答案、解析分离
- 单位标准化：如 `mm Hg` -> `mmHg`、`mg / dL` -> `mg/dL`
- Markdown 清理：恢复标题、列表、表格和题目结构
- 输出前自检：检查残留扁平化医学符号、合并选项、单位格式和隐私风险

## English

This project is not primarily about choosing an OCR engine. It focuses on cleaning, correcting, structuring, and quality-checking medical OCR text after OCR has already been produced.

It guides Codex to:

- correct biomedical notation, such as `PaCO2` -> `PaCO₂` and `HCO3-` -> `HCO₃⁻`
- recover question-bank structure: number, stem, options, answer, and explanation
- standardize units, such as `mm Hg` -> `mmHg` and `mg / dL` -> `mg/dL`
- clean Markdown structure for notes, textbook pages, and question banks
- run pre-output QA checks for flattened notation, merged options, unit formatting, and privacy risks

## 功能特点 / Features

- 常见医学符号映射表和保守纠错规则
- 血气、电解质、甲功、肺功能、糖化血红蛋白、免疫标志物、核医学同位素等 OCR 易错项处理
- 简单题库 OCR 单行恢复为结构化 Markdown
- 单位空格和大小写标准化
- `postprocess_medical_ocr.py` 可作为命令行后处理脚本
- `test_medical_corrector.py` 覆盖 20+ 个医学 OCR 易错例子

- Common biomedical notation mapping and conservative correction rules
- Corrections for ABG, electrolytes, thyroid hormones, pulmonary function, HbA1c, immune markers, and nuclear medicine isotopes
- Simple question-bank OCR recovery into structured Markdown
- Unit spacing and casing normalization
- `postprocess_medical_ocr.py` as a command-line post-processing script
- `test_medical_corrector.py` covering 20+ common medical OCR error cases

## 安装 / Installation

使用 Codex 自带的 skill installer 安装：

```powershell
python C:\Users\16648\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --url https://github.com/fangzh05/medical-ocr-router-skill/tree/main/skills/medical-ocr-router
```

安装后重启 Codex。  
Restart Codex after installation.

## 使用方式 / Usage

在 Codex 中可以这样调用：

```text
Use $medical-ocr-router to post-process this medical OCR text, normalize biomedical notation, recover question structure, standardize units, and run QA checks.
```

中文请求示例：

```text
请用 $medical-ocr-router 处理这段医学 OCR 文本，纠正 PaCO2、HCO3-、FEV1/FVC 等医学符号，恢复题库结构，并做输出前检查。
```

命令行脚本示例：

```powershell
python skills\medical-ocr-router\scripts\postprocess_medical_ocr.py input.txt -o output.md
```

也可以通过标准输入使用：

```powershell
Get-Content input.txt | python skills\medical-ocr-router\scripts\postprocess_medical_ocr.py
```

## 验证 / Validation

提交修改前运行：

```powershell
python skills\medical-ocr-router\scripts\test_medical_corrector.py
python C:\Users\16648\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\medical-ocr-router
```

第一条命令验证医学 OCR 后处理规则。第二条命令验证 Codex skill 元数据和结构。

## 示例 / Examples

| OCR text | Corrected text |
|---|---|
| PaCO2 | PaCO₂ |
| HCO3- | HCO₃⁻ |
| SaO2/SpO2 | SaO₂/SpO₂ |
| FEV1/FVC | FEV₁/FVC |
| T3/T4 | T₃/T₄ |
| 131I | ¹³¹I |
| 99mTc | ⁹⁹ᵐTc |

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

## 局限性 / Limitations

- 本项目不内置 OCR 引擎，默认处理已经 OCR 出来的文本。
- 后处理规则不能替代人工医学审校。
- 对 `T3/T4`、`CO2/O2` 这类可能有多重含义的文本，会尽量根据上下文保守处理。
- 复杂表格、公式图片和严重错乱的 OCR 文本仍需要人工复核。

- This project does not include an OCR engine; it assumes OCR text already exists.
- Post-processing rules do not replace medical review.
- Ambiguous tokens such as `T3/T4` and `CO2/O2` are handled conservatively using context where possible.
- Complex tables, formula images, and severely corrupted OCR text still need human review.

## 隐私提醒 / Privacy Notice

不要上传患者隐私、真实病历、身份证号、手机号、医院号、检查报告原图或其他敏感信息。公开 issue、PR 和示例文件中只能使用脱敏样例或合成数据。

Do not upload patient privacy data, real medical records, ID numbers, phone numbers, hospital IDs, original examination report images, or other sensitive information. Public issues, pull requests, and examples should use only de-identified samples or synthetic data.

## 后续计划 / Roadmap

- 扩展医学符号和单位标准化规则。
- 增加更多中文医学题库结构恢复样例。
- 支持更复杂的多题连续文本整理。
- 增加可选的 JSON QA 报告输出。

- Expand biomedical notation and unit normalization rules.
- Add more Chinese medical question-bank recovery examples.
- Support more complex multi-question OCR text.
- Add optional JSON QA report output.

## 开源协议 / License

本项目使用 MIT License。详见 [LICENSE](LICENSE)。  
This project is licensed under the MIT License. See [LICENSE](LICENSE).

