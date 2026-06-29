from __future__ import annotations

from medical_symbol_corrector import correct_medical_symbols, correct_text
from postprocess_medical_ocr import postprocess_text


def correct_biomedical_notation(text: str) -> str:
    return correct_text(text)


def correction_report(text: str) -> str:
    return postprocess_text(text)


def quality_warnings(text: str) -> list[str]:
    return correct_medical_symbols(text).warnings


if __name__ == "__main__":
    import sys

    sys.stdout.write(correction_report(sys.stdin.read()))

