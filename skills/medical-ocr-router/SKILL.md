---
name: medical-ocr-router
description: Medical OCR Corrector and QA skill for post-processing OCR text from medical textbooks, lecture slides, question banks, scanned PDFs, and screenshots. Use when Codex needs to normalize biomedical notation, repair OCR-flattened subscripts and superscripts, restore question-bank structure, standardize units, produce Markdown, and run output quality checks.
---

# Medical OCR Corrector & QA

Use this skill after OCR text has already been produced from medical textbooks, lecture slides, scanned PDFs, screenshots, or question banks. Focus on correcting, structuring, standardizing, and checking the text. Do not spend the main effort choosing OCR engines unless the source text is clearly unusable.

## Core Workflow

1. Preserve the original meaning and do not invent missing content.
2. Normalize OCR-flattened biomedical notation.
3. Restore question-bank structure when the text contains numbered stems, choices, answers, or explanations.
4. Standardize common medical units and spacing.
5. Rebuild clean Markdown with headings, lists, tables, and question sections.
6. Run the pre-output QA checklist.
7. Mark uncertain corrections explicitly, for example `[疑似：PaCO₂，需人工复核]`.

## Bundled Resources

- Use `scripts/postprocess_medical_ocr.py` for deterministic text post-processing, notation normalization, simple question structure recovery, and QA warnings.
- `scripts/medical_corrector.py` is a compatibility wrapper for older calls.
- Read `references/biomedical-notation.md` for more notation examples.
- Read `references/ocr-routing.md` only when the OCR source text is too broken to correct. The skill's main job starts after OCR.

## Medical Symbol Mapping

Apply these common OCR corrections conservatively. Do not convert unrelated chapter numbers, years, table numbers, case numbers, or cancer staging unless the context supports a biomedical notation reading.

| OCR text | Correct form | Notes |
|---|---|---|
| PaCO2 | PaCO₂ | arterial carbon dioxide |
| PaO2 | PaO₂ | arterial oxygen |
| SaO2 | SaO₂ | arterial oxygen saturation |
| SpO2 | SpO₂ | pulse oxygen saturation |
| HCO3- | HCO₃⁻ | bicarbonate |
| CO2 | CO₂ | correct in respiratory, acid-base, chemistry, or anesthesia context |
| O2 | O₂ | correct in oxygenation, ventilation, or respiratory context |
| FEV1/FVC | FEV₁/FVC | pulmonary function |
| FEV1 | FEV₁ | pulmonary function |
| HbA1c | HbA₁c | diabetes marker |
| T3/T4 | T₃/T₄ | thyroid hormone context |
| FT3/FT4 | FT₃/FT₄ | thyroid hormone context |
| Na+ | Na⁺ | electrolyte |
| K+ | K⁺ | electrolyte |
| Cl- | Cl⁻ | electrolyte |
| Ca2+ | Ca²⁺ | electrolyte |
| Mg2+ | Mg²⁺ | electrolyte |
| CD4+ | CD4⁺ | immunology marker |
| CD8+ | CD8⁺ | immunology marker |
| TNF-a | TNF-α | cytokine |
| IFN-gamma | IFN-γ | cytokine |
| 131I | ¹³¹I | isotope |
| 99mTc | ⁹⁹ᵐTc | isotope |

Required example outcomes:

- `PaCO2` -> `PaCO₂`
- `HCO3-` -> `HCO₃⁻`
- `SaO2/SpO2` -> `SaO₂/SpO₂`
- `FEV1/FVC` -> `FEV₁/FVC`
- `T3/T4` -> `T₃/T₄`
- `131I` -> `¹³¹I`
- `99mTc` -> `⁹⁹ᵐTc`

## Unit Standardization

Normalize spacing and common OCR variants without changing values:

- `mm Hg` -> `mmHg`
- `mmol / L` -> `mmol/L`
- `mEq / L` -> `mEq/L`
- `mg / dL` -> `mg/dL`
- `ug/dL`, `mcg/dL` -> `μg/dL`
- `ug/L`, `mcg/L` -> `μg/L`
- keep numeric ranges readable, for example `35 - 45 mmHg` -> `35-45 mmHg`

Do not infer units that are missing from the OCR text.

## Question-Bank Structure Recovery

When OCR text appears to contain exam questions, restore a stable Markdown structure:

```text
## 第 X 题
【题型】未在原文中识别到
【题干】...
【选项】
A. ...
B. ...
C. ...
D. ...
E. ...
【答案】...
【解析】...
```

Rules:

- Preserve the original question number.
- Keep the stem separate from options.
- Put each option on its own line.
- Keep answer and explanation separate when present.
- If answer or explanation is missing, write `未在原文中识别到`.
- Do not invent answer choices, answers, explanations, diagnoses, or reasoning.
- If the OCR text merges options into one line, split only when option markers such as `A.`、`B.`、`C.`、`D.` are clear.

## Output Markdown

For textbook or lecture content:

- Keep headings and subheadings.
- Keep tables as Markdown only when rows and columns are clear.
- Keep uncertain formulas as plain text plus a review marker.
- Preserve page numbers when present.

For question banks:

- Use one `## 第 X 题` section per question.
- Use bracket labels such as `【题干】` and `【选项】`.
- Do not merge options into paragraph text.

## Pre-Output QA Checklist

Before returning the final result, check:

- Biomedical notation: no obvious flattened forms such as `PaCO2`, `HCO3-`, `SpO2`, `FEV1`, `HbA1c`, `Ca2+`, `131I`, or `99mTc` remain unless intentionally preserved.
- Context safety: `T3`, `T4`, `CO2`, and `O2` were corrected only when context supports it or when they occur in a known medical symbol pattern.
- Question structure: question number, stem, choices, answer, and explanation are not merged.
- Units: common spacing variants such as `mm Hg`, `mmol / L`, and `mg / dL` are normalized.
- Tables: table-like content was not flattened into unreadable lines.
- Uncertainty: unreadable or ambiguous text is marked instead of guessed.
- Privacy: patient identifiers, real medical records, phone numbers, hospital IDs, and report images are not included in public outputs.

If issues remain, append a short `## OCR质量检查警告` section with actionable warnings.

