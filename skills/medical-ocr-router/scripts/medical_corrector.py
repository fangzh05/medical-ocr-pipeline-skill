from __future__ import annotations

from postprocess_medical_ocr import (
    normalize_biomedical_notation as correct_biomedical_notation,
    postprocess_text,
    quality_warnings,
)


def correction_report(text: str) -> str:
    return postprocess_text(text).text


if __name__ == "__main__":
    import sys

    sys.stdout.write(correction_report(sys.stdin.read()))

