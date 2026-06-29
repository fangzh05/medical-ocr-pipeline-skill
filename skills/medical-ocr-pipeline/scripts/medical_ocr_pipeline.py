from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from medical_symbol_corrector import correct_medical_symbols
from ocr_risk_detector import Risk, detect_block_risks
from question_structure_rebuilder import rebuild_question_markdown


@dataclass
class OCRBlock:
    bbox: list[list[float]]
    text: str
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {"bbox": self.bbox, "text": self.text, "confidence": self.confidence}


@dataclass
class RefinedBlock:
    bbox: list[list[float]]
    original_text: str
    final_text: str
    confidence: float
    risks: list[dict[str, Any]] = field(default_factory=list)
    rerecognized_text: str | None = None
    decision: str = "kept_or_corrected"
    warnings: list[str] = field(default_factory=list)


@dataclass
class PipelineResult:
    final_markdown: str
    blocks: list[RefinedBlock]
    risks: list[dict[str, Any]]
    qa_warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "final_markdown": self.final_markdown,
            "blocks": [asdict(block) for block in self.blocks],
            "risks": self.risks,
            "qa_warnings": self.qa_warnings,
        }


OCRFunc = Callable[[Path], list[OCRBlock]]


def parse_paddleocr_result(result: Any) -> list[OCRBlock]:
    blocks: list[OCRBlock] = []
    pages = result if isinstance(result, list) else [result]
    for page in pages:
        if page is None:
            continue
        if isinstance(page, dict) and "rec_texts" in page:
            for bbox, text, score in zip(page.get("rec_boxes", []), page.get("rec_texts", []), page.get("rec_scores", [])):
                x1, y1, x2, y2 = bbox
                blocks.append(OCRBlock(bbox=[[x1, y1], [x2, y1], [x2, y2], [x1, y2]], text=str(text), confidence=float(score)))
            continue
        for item in page:
            try:
                bbox = item[0]
                text = item[1][0]
                confidence = item[1][1]
            except Exception:
                continue
            blocks.append(OCRBlock(bbox=bbox, text=str(text), confidence=float(confidence)))
    return blocks


def run_paddleocr(image_path: Path) -> list[OCRBlock]:
    try:
        from paddleocr import PaddleOCR
    except Exception as exc:
        raise RuntimeError("PaddleOCR is not available in the current environment. Run mock-based tests instead.") from exc

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    result = ocr.ocr(str(image_path), cls=True)
    return parse_paddleocr_result(result)


def _bbox_rect(bbox: list[list[float]]) -> tuple[int, int, int, int]:
    xs = [point[0] for point in bbox]
    ys = [point[1] for point in bbox]
    return int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))


def crop_and_enhance(image_path: Path, bbox: list[list[float]], output_path: Path, scale: int = 3) -> Path:
    try:
        from PIL import Image, ImageEnhance, ImageFilter
    except Exception as exc:
        raise RuntimeError("Pillow is required for crop enhancement.") from exc

    image = Image.open(image_path)
    left, top, right, bottom = _bbox_rect(bbox)
    pad = 4
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(image.width, right + pad)
    bottom = min(image.height, bottom + pad)
    crop = image.crop((left, top, right, bottom))
    crop = crop.resize((max(1, crop.width * scale), max(1, crop.height * scale)))
    crop = crop.convert("L")
    crop = ImageEnhance.Contrast(crop).enhance(1.6)
    crop = crop.filter(ImageFilter.SHARPEN)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    crop.save(output_path)
    return output_path


def _choose_text(initial_text: str, rerecognized_text: str | None, context: str) -> tuple[str, str, list[str]]:
    warnings: list[str] = []
    initial = correct_medical_symbols(initial_text)
    if not rerecognized_text:
        return initial.text, "corrected_initial", initial.warnings

    second = correct_medical_symbols(rerecognized_text)
    if second.text == initial.text:
        return initial.text, "initial_and_crop_agree", initial.warnings + second.warnings

    initial_risk_count = len(initial.warnings)
    second_risk_count = len(second.warnings)
    if second_risk_count < initial_risk_count or len(second.text) > len(initial.text):
        warnings.extend(second.warnings)
        warnings.append(f"Crop OCR differed from initial OCR; chose crop text after context check: {initial.text} -> {second.text}")
        return second.text, "chose_crop_ocr", warnings

    warnings.extend(initial.warnings)
    warnings.append(f"Initial OCR conflicts with crop OCR; kept initial text and requires review: {initial.text} vs {second.text}")
    return initial.text, "conflict_kept_initial", warnings


def refine_blocks(
    blocks: list[OCRBlock],
    image_path: Path | None = None,
    debug_dir: Path | None = None,
    crop_ocr_func: OCRFunc | None = None,
    confidence_threshold: float = 0.85,
) -> list[RefinedBlock]:
    block_dicts = [block.to_dict() for block in blocks]
    risks = detect_block_risks(block_dicts, confidence_threshold=confidence_threshold)
    risks_by_block: dict[int, list[Risk]] = {}
    for risk in risks:
        if risk.block_index is not None:
            risks_by_block.setdefault(risk.block_index, []).append(risk)

    refined: list[RefinedBlock] = []
    context = "\n".join(block.text for block in blocks)
    for index, block in enumerate(blocks):
        block_risks = risks_by_block.get(index, [])
        rerecognized_text: str | None = None
        if block_risks and image_path and debug_dir and crop_ocr_func:
            crop_path = crop_and_enhance(image_path, block.bbox, debug_dir / "crops" / f"block_{index:04d}.png")
            crop_blocks = crop_ocr_func(crop_path)
            rerecognized_text = " ".join(crop_block.text for crop_block in crop_blocks).strip() or None
        final_text, decision, warnings = _choose_text(block.text, rerecognized_text, context)
        refined.append(
            RefinedBlock(
                bbox=block.bbox,
                original_text=block.text,
                final_text=final_text,
                confidence=block.confidence,
                risks=[risk.to_dict() for risk in block_risks],
                rerecognized_text=rerecognized_text,
                decision=decision,
                warnings=warnings,
            )
        )
    return refined


def build_outputs(refined_blocks: list[RefinedBlock]) -> PipelineResult:
    text = "\n".join(block.final_text for block in refined_blocks)
    question_result = rebuild_question_markdown(text)
    final_markdown = question_result.markdown
    qa_warnings = question_result.warnings[:]
    all_risks: list[dict[str, Any]] = []
    for block in refined_blocks:
        all_risks.extend(block.risks)
        qa_warnings.extend(block.warnings)
    if not qa_warnings:
        qa_warnings.append("未发现明显 OCR 风险，但医学内容仍建议人工复核。")
    return PipelineResult(final_markdown=final_markdown, blocks=refined_blocks, risks=all_risks, qa_warnings=qa_warnings)


def qa_report_markdown(result: PipelineResult) -> str:
    lines = ["# QA Report", "", "## Warnings"]
    for warning in result.qa_warnings:
        lines.append(f"- {warning}")
    lines.extend(["", "## Risks"])
    if result.risks:
        for risk in result.risks:
            lines.append(f"- `{risk['token']}`: {risk['risk_type']} -> {risk['suggestion']} ({risk['reason']})")
    else:
        lines.append("- No high-risk tokens detected.")
    return "\n".join(lines) + "\n"


def run_pipeline(
    input_path: Path,
    ocr_func: OCRFunc = run_paddleocr,
    crop_ocr_func: OCRFunc | None = None,
    debug_dir: Path | None = None,
    confidence_threshold: float = 0.85,
) -> PipelineResult:
    blocks = ocr_func(input_path)
    refined = refine_blocks(
        blocks,
        image_path=input_path,
        debug_dir=debug_dir,
        crop_ocr_func=crop_ocr_func or ocr_func,
        confidence_threshold=confidence_threshold,
    )
    return build_outputs(refined)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the medical OCR refinement pipeline.")
    parser.add_argument("input", help="Input image path or page image rendered from PDF.")
    parser.add_argument("--output", default="output.md", help="Markdown output path.")
    parser.add_argument("--json", default="output.json", help="JSON output path.")
    parser.add_argument("--qa", default="qa_report.md", help="QA report output path.")
    parser.add_argument("--debug-dir", default="debug", help="Directory for debug crops.")
    parser.add_argument("--confidence-threshold", type=float, default=0.85)
    args = parser.parse_args(argv)

    try:
        result = run_pipeline(
            Path(args.input),
            debug_dir=Path(args.debug_dir),
            confidence_threshold=args.confidence_threshold,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    Path(args.output).write_text(result.final_markdown, encoding="utf-8")
    Path(args.json).write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.qa).write_text(qa_report_markdown(result), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

