from __future__ import annotations

import argparse
import sys
from pathlib import Path

from medical_symbol_corrector import correct_medical_symbols
from ocr_risk_detector import detect_text_risks
from question_structure_rebuilder import rebuild_question_markdown


def postprocess_text(text: str, include_warnings: bool = True) -> str:
    correction = correct_medical_symbols(text)
    question = rebuild_question_markdown(correction.text)
    warnings = correction.warnings + question.warnings
    warnings.extend(risk.reason for risk in detect_text_risks(question.markdown))
    if include_warnings and warnings:
        warning_block = "\n".join(f"- {warning}" for warning in dict.fromkeys(warnings))
        return f"{question.markdown.rstrip()}\n\n---\n\n## OCR质量检查警告\n\n{warning_block}\n"
    return question.markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Text-only medical OCR post-processing compatibility entrypoint.")
    parser.add_argument("input", nargs="?", help="Input text file. Reads stdin when omitted.")
    parser.add_argument("-o", "--output", help="Output text file. Writes stdout when omitted.")
    parser.add_argument("--no-warnings", action="store_true")
    args = parser.parse_args(argv)

    text = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
    output = postprocess_text(text, include_warnings=not args.no_warnings)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

