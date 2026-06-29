---
name: medical-ocr-pipeline
description: >
  Medical OCR Pipeline Skill for Codex. Use for medical textbooks, lecture
  slides, scanned PDFs, screenshots, and question banks when Codex needs an OCR
  refinement pipeline with image preprocessing, initial OCR block capture with
  bbox/text/confidence, medical risk detection, low-confidence crop
  re-recognition, context-aware biomedical symbol correction,
  question/table/paragraph reconstruction, Markdown/JSON output, and QA
  warnings.
---

# Medical OCR Pipeline Skill

Use this skill to run or design a medical OCR refinement pipeline, not just post-processing. It is for medical textbooks, lecture slides, question-bank screenshots, scanned PDFs, and medical screenshots where one plain OCR pass is not reliable enough.

This skill implements a medical OCR refinement pipeline, not just post-processing.

## Technical Boundary

- This skill does not modify PaddleOCR model weights.
- This skill does not guarantee perfect OCR.
- This skill improves reliability by using local re-recognition, medical-symbol-aware correction, context validation, and QA warnings.
- If a symbol or token cannot be confirmed, do not silently guess. Mark it as `[需人工复核: ...]`.

## Core Pipeline

Input medical textbook / lecture slide / question-bank screenshot / scanned PDF page
-> image preprocessing
-> initial OCR
-> keep OCR blocks with `bbox`, `text`, and `confidence`
-> detect low-confidence regions and medical-symbol risk points
-> crop risk bboxes
-> apply 2x or 3x enlargement, sharpening, contrast enhancement, grayscale, and optional binarization
-> re-run OCR on crop regions
-> compare initial OCR and crop OCR
-> generate `final_text` using medical-symbol rules and context rules
-> rebuild question-bank, table, and paragraph structure
-> output Markdown and JSON
-> generate a QA report

## Bundled Scripts

- `scripts/medical_ocr_pipeline.py`: main CLI and orchestration layer.
- `scripts/medical_symbol_corrector.py`: context-aware biomedical symbol correction.
- `scripts/ocr_risk_detector.py`: high-risk medical token and OCR-confusion detector.
- `scripts/question_structure_rebuilder.py`: question-bank structure recovery and warnings.
- `scripts/postprocess_medical_ocr.py`: text-only post-processing compatibility entrypoint.
- `scripts/test_medical_ocr_pipeline.py`: mock-based tests that do not require PaddleOCR.

## Medical High-Risk Tokens

Treat these tokens and patterns as high-risk during OCR review:

- Blood gas and respiratory: `PaCO2`, `PaO2`, `SpO2`, `SaO2`, `EtCO2`, `PETCO2`, `FiO2`, `HCO3-`, `HCO3`, `CO2`, `O2`
- Pulmonary function: `FEV1`, `FEV1/FVC`
- Endocrine: `T3`, `T4`, `FT3`, `FT4`
- Nuclear medicine: `99mTc`, `99rnTc`, `131I`, `I131`, `18F-FDG`
- Greek and receptors: `α`, `β`, `γ`, `μ`, `u`, `β2 receptor`, `α1 receptor`
- Units: `℃`, `°C`, `mmHg`, `cmH2O`, `mg/kg`, `μg/kg`, `ug/kg`, `mmol/L`
- Electrolytes and ions: `Na+`, `K+`, `Cl-`, `Ca2+`, `Mg2+`, `H+`, `OH-`

## Context-Aware Correction Rules

Correct only when the token is a known medical symbol or the surrounding context supports the correction.

Required examples:

- `PaCO2` -> `PaCO₂`
- `PaO2` -> `PaO₂`
- `SpO2` -> `SpO₂`
- `SaO2` -> `SaO₂`
- `EtCO2` -> `EtCO₂`
- `PETCO2` -> `PETCO₂`
- `HCO3-` -> `HCO₃⁻`
- `HCO3` -> `HCO₃⁻` only in acid-base, blood gas, bicarbonate, or respiratory context
- `CO2潴留` -> `CO₂潴留`
- `O2吸入` -> `O₂吸入`
- `FEV1/FVC` -> `FEV₁/FVC`
- `T3/T4` -> `T₃/T₄` only in thyroid context
- `99mTc` -> `⁹⁹ᵐTc`
- `99rnTc` -> `⁹⁹ᵐTc` with a QA warning
- `131I` and `I131` -> `¹³¹I`
- `18F-FDG` -> `¹⁸F-FDG`
- `Ca2+`, `Mg2+`, `Na+`, `K+`, `Cl-`, `H+`, `OH-` -> ion notation
- `TNF-a`, `IFN-gamma`, `TGF-beta` -> Greek-letter cytokine notation

Do not correct:

- tumor staging such as `肿瘤T3期` or `T4期`
- question numbers such as `第3题`
- years such as `2024`
- model numbers, filenames, table numbers, chapter numbers, or case numbers

## Crop Re-Recognition Rules

Crop and re-run OCR for:

- any OCR block below the confidence threshold
- blocks containing high-risk medical tokens
- blocks containing suspected superscripts/subscripts, unit problems, Greek letters, isotopes, or OCR confusions

For crop enhancement:

- enlarge 2x or 3x
- sharpen moderately
- enhance contrast moderately
- grayscale when useful
- binarize only when it improves readability
- avoid aggressive processing that destroys subscripts, superscripts, minus signs, plus signs, or Greek letters

If initial OCR and crop OCR conflict:

- prefer the clearer result only when confidence or context supports it
- use medical symbol rules and surrounding text to decide
- if unresolved, preserve the safer source and add a QA warning
- never fabricate missing content

## Question-Bank Recovery

Recover:

- question number
- question type
- stem
- A/B/C/D/E options
- answer line
- explanation line
- missing option warnings
- skipped question number warnings
- merged option warnings

Use this output shape:

```text
## 第 X 题
【题型】
A1 / A2 / A3 / B1 / X型题 / 判断题 / 简答题
【题干】
...
【选项】
A. ...
B. ...
C. ...
D. ...
E. ...
【答案】
...
【解析】
...
【OCR复核】
- ...
```

If answer or explanation is not recognized, write `未在原文中识别到`.

## Output Requirements

Generate:

- `output.md`: refined Markdown
- `output.json`: OCR blocks, risks, refinement decisions, final text, and QA warnings
- `qa_report.md`: concise warnings and manual-review notes
- `debug/crops/`: cropped high-risk regions when image input is available

## CLI

```powershell
python scripts\medical_ocr_pipeline.py input.png --output output.md --json output.json --qa qa_report.md --debug-dir debug
```

If PaddleOCR is not installed, explain that real OCR cannot run in the current environment and still run mock-based tests for the pipeline logic.
