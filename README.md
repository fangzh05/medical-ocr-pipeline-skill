# Medical OCR Router Skill

Codex skill for high-fidelity OCR of medical screenshots, scanned PDFs, textbook pages, slides, and question-bank images.

It helps Codex route OCR work across:

- standard text OCR
- formula-sensitive recognition
- table recognition
- document layout parsing
- biomedical notation correction
- Markdown assembly and quality checks

The skill is optimized for Chinese medical learning materials where notation such as `PaCO2`, `HCO3-`, `SpO2`, `FEV1/FVC`, and `HbA1c` must be preserved or restored as `PaCO₂`, `HCO₃⁻`, `SpO₂`, `FEV₁/FVC`, and `HbA₁c`.

## Repository Layout

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

## Install

After this repository is on GitHub, install the skill with:

```powershell
python C:\Users\16648\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --url https://github.com/fangzh05/medical-ocr-router-skill/tree/main/skills/medical-ocr-router
```

Then restart Codex.

## Local Validation

```powershell
python skills\medical-ocr-router\scripts\test_medical_corrector.py
python C:\Users\16648\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\medical-ocr-router
```
