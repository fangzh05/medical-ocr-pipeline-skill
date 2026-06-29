# Medical OCR Pipeline Skill for Codex / 医学 OCR 识别-复核-纠错流水线 Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](RELEASE_NOTES_v0.1.0.md)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827.svg)](skills/medical-ocr-pipeline/SKILL.md)

## English

This skill implements a medical OCR refinement pipeline, not just post-processing.

It improves medical OCR reliability through local re-recognition, crop-based refinement, medical-symbol-aware correction, context validation, and QA warnings. It is designed for medical textbooks, lecture slides, scanned PDFs, screenshots, and question banks.

It does not modify PaddleOCR model weights. It does not guarantee perfect OCR. Unconfirmed content must be marked for manual review.

## 中文

本项目诞生之因是为了扫描课本整理成md格式，比起一个ocr调用skills更像是一个专门为了识别各种在医学课本中常见的特殊符号的处理skills

它通过局部裁剪、图像增强、二次识别、医学符号规则、上下文校验和 QA 自检，提高医学教材、课件、题库截图和扫描 PDF 的 OCR 质量。

它不会修改 PaddleOCR 模型权重，也不保证 OCR 绝对正确。无法确认的内容必须输出复核提示。

## Pipeline

```text
medical image / PDF page
-> preprocessing
-> initial OCR
-> keep bbox/text/confidence blocks
-> detect low-confidence and high-risk medical tokens
-> crop risk bboxes
-> enhance crops
-> second OCR
-> compare OCR passes
-> context-aware medical correction
-> rebuild question/table/paragraph structure
-> output Markdown + JSON + QA report
```

## Features / 功能

- Initial OCR block preservation with `bbox`, `text`, and `confidence`
- Low-confidence and high-risk token detection
- Crop-based local re-recognition design
- Context-aware biomedical notation correction
- OCR confusion detection: `O/0`, `l/1`, `I/1`, `μ/u`, `m/rn`
- Question-bank structure recovery
- Markdown, JSON, QA report, and debug crop outputs
- Mock-based tests that do not require PaddleOCR

## Installation / 安装

```powershell
python C:\Users\16648\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --url https://github.com/fangzh05/medical-ocr-pipeline-skill/tree/main/skills/medical-ocr-pipeline
```

Restart Codex after installation.  
安装后重启 Codex。

## Codex Usage / Codex 使用方式

```text
Use $medical-ocr-pipeline to refine this medical OCR task with risk detection, crop re-recognition, context-aware correction, structured output, and QA warnings.
```

```text
请用 $medical-ocr-pipeline 处理这张医学题库截图：先做 OCR 风险检测，对高风险区域局部复识别，再进行医学符号纠错、题库结构恢复和 QA 自检。
```

## CLI

```powershell
python skills\medical-ocr-pipeline\scripts\medical_ocr_pipeline.py input.png --output output.md --json output.json --qa qa_report.md --debug-dir debug
```

If PaddleOCR is unavailable, run the mock-based tests to verify pipeline logic:

```powershell
python skills\medical-ocr-pipeline\scripts\test_medical_ocr_pipeline.py
python C:\Users\16648\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\medical-ocr-pipeline
```

## Outputs / 输出文件

- `output.md`: refined Markdown result
- `output.json`: OCR blocks, risks, decisions, final text, QA warnings
- `qa_report.md`: human-readable QA warnings
- `debug/crops/`: cropped high-risk OCR regions for review

## Examples / 示例

- [Blood gas OCR example](examples/blood_gas_ocr_example.md)
- [Nuclear medicine OCR example](examples/nuclear_medicine_ocr_example.md)
- [Anesthesia monitoring OCR example](examples/anesthesia_monitoring_ocr_example.md)
- [Question bank OCR example](examples/question_bank_ocr_example.md)

## Repository Layout / 仓库结构

```text
medical-ocr-pipeline-skill/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── RELEASE_NOTES_v0.1.0.md
├── examples/
└── skills/
    └── medical-ocr-pipeline/
        ├── SKILL.md
        ├── agents/
        ├── references/
        └── scripts/
```

## Limitations / 局限性

- This skill does not modify PaddleOCR model weights.
- It does not guarantee perfect OCR.
- Crop re-recognition requires a local OCR environment such as PaddleOCR.
- The rules improve reliability but do not replace medical review.
- Unconfirmed tokens must be marked as `[需人工复核: ...]`.

## License / 开源协议

MIT License. See [LICENSE](LICENSE).

