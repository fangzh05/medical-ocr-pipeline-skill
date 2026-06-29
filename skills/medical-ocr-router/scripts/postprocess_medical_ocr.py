from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TOKEN_LEFT = r"(?<![A-Za-z0-9])"
TOKEN_RIGHT = r"(?![A-Za-z0-9])"


DIRECT_REPLACEMENTS = {
    "PaCO2": "PaCO₂",
    "PaO2": "PaO₂",
    "PvCO2": "PvCO₂",
    "PvO2": "PvO₂",
    "PACO2": "PACO₂",
    "PAO2": "PAO₂",
    "PCO2": "PCO₂",
    "PO2": "PO₂",
    "SpO2": "SpO₂",
    "SaO2": "SaO₂",
    "SvO2": "SvO₂",
    "ScvO2": "ScvO₂",
    "EtCO2": "EtCO₂",
    "PETCO2": "PETCO₂",
    "FiO2": "FiO₂",
    "FIO2": "FiO₂",
    "HCO3-": "HCO₃⁻",
    "HCO3−": "HCO₃⁻",
    "Na+": "Na⁺",
    "K+": "K⁺",
    "Cl-": "Cl⁻",
    "Cl−": "Cl⁻",
    "Ca2+": "Ca²⁺",
    "Ca++": "Ca²⁺",
    "Mg2+": "Mg²⁺",
    "Mg++": "Mg²⁺",
    "Fe2+": "Fe²⁺",
    "Fe3+": "Fe³⁺",
    "H+": "H⁺",
    "OH-": "OH⁻",
    "OH−": "OH⁻",
    "FEV1/FVC": "FEV₁/FVC",
    "FEV1": "FEV₁",
    "HbA1c": "HbA₁c",
    "HbA1C": "HbA₁c",
    "CD4+": "CD4⁺",
    "CD8+": "CD8⁺",
    "CD20+": "CD20⁺",
    "FT3": "FT₃",
    "FT4": "FT₄",
    "rT3": "rT₃",
    "T3/T4": "T₃/T₄",
    "131I": "¹³¹I",
    "123I": "¹²³I",
    "99mTc": "⁹⁹ᵐTc",
    "18F-FDG": "¹⁸F-FDG",
    "67Ga": "⁶⁷Ga",
    "201Tl": "²⁰¹Tl",
}

SUSPICIOUS_PATTERNS = [
    r"\bPaCO2\b",
    r"\bPaO2\b",
    r"\bSpO2\b",
    r"\bSaO2\b",
    r"\bHCO3-?\b",
    r"\bFEV1\b",
    r"\bHbA1c\b",
    r"\bCa2\+\b",
    r"\bMg2\+\b",
    r"\bCD4\+\b",
    r"\bCD8\+\b",
    r"\b99mTc\b",
    r"\b131I\b",
    r"\bmm\s+Hg\b",
    r"\bmmol\s*/\s*L\b",
    r"\bmg\s*/\s*dL\b",
]

QUESTION_MARKER = re.compile(r"(?m)^\s*(?:第\s*)?(\d{1,3})\s*[.、．]\s*(.+)")
OPTION_MARKER = re.compile(r"([A-E])\s*[.、．]\s*")


@dataclass
class PostprocessResult:
    text: str
    warnings: list[str]


def _has_context(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _replace_token(text: str, source: str, target: str) -> str:
    pattern = TOKEN_LEFT + re.escape(source) + TOKEN_RIGHT
    return re.sub(pattern, target, text)


def normalize_biomedical_notation(text: str) -> str:
    for source, target in sorted(DIRECT_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
        text = _replace_token(text, source, target)

    text = re.sub(TOKEN_LEFT + r"TNF-a" + TOKEN_RIGHT, "TNF-α", text)
    text = re.sub(TOKEN_LEFT + r"TNF-alpha" + TOKEN_RIGHT, "TNF-α", text, flags=re.IGNORECASE)
    text = re.sub(TOKEN_LEFT + r"IFN-gamma" + TOKEN_RIGHT, "IFN-γ", text, flags=re.IGNORECASE)
    text = re.sub(TOKEN_LEFT + r"TGF-beta" + TOKEN_RIGHT, "TGF-β", text, flags=re.IGNORECASE)

    thyroid_context = _has_context(
        text,
        r"甲状腺|甲亢|甲减|Graves|桥本|TSH|thyroid|hyperthyroidism|hypothyroidism|内分泌",
    )
    if thyroid_context:
        text = re.sub(TOKEN_LEFT + r"T3" + TOKEN_RIGHT, "T₃", text)
        text = re.sub(TOKEN_LEFT + r"T4" + TOKEN_RIGHT, "T₄", text)

    respiratory_context = _has_context(
        text,
        r"呼吸|氧|二氧化碳|通气|换气|血气|酸中毒|碱中毒|麻醉|肺|ventilation|oxygen|carbon dioxide|ABG",
    )
    if respiratory_context:
        text = re.sub(TOKEN_LEFT + r"CO2" + TOKEN_RIGHT, "CO₂", text)
        text = re.sub(TOKEN_LEFT + r"O2" + TOKEN_RIGHT, "O₂", text)
        text = re.sub(TOKEN_LEFT + r"HCO3" + TOKEN_RIGHT, "HCO₃⁻", text)

    receptor_context = _has_context(text, r"受体|receptor|adrenergic|肾上腺素")
    if receptor_context:
        text = re.sub(r"\balpha1\b", "α₁", text, flags=re.IGNORECASE)
        text = re.sub(r"\balpha2\b", "α₂", text, flags=re.IGNORECASE)
        text = re.sub(r"\bbeta1\b", "β₁", text, flags=re.IGNORECASE)
        text = re.sub(r"\bbeta2\b", "β₂", text, flags=re.IGNORECASE)
        text = re.sub(r"\bβ1\b", "β₁", text)
        text = re.sub(r"\bβ2\b", "β₂", text)

    return text


def standardize_units(text: str) -> str:
    replacements = [
        (r"\bmm\s+Hg\b", "mmHg"),
        (r"\bmmol\s*/\s*L\b", "mmol/L"),
        (r"\bmEq\s*/\s*L\b", "mEq/L"),
        (r"\bmg\s*/\s*dL\b", "mg/dL"),
        (r"\bug\s*/\s*dL\b", "μg/dL"),
        (r"\bmcg\s*/\s*dL\b", "μg/dL"),
        (r"\bug\s*/\s*L\b", "μg/L"),
        (r"\bmcg\s*/\s*L\b", "μg/L"),
        (r"\b(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(mmHg|mmol/L|mEq/L|mg/dL|μg/dL|μg/L)\b", r"\1-\2 \3"),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def recover_question_structure(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) != 1:
        return text

    line = lines[0]
    match = QUESTION_MARKER.match(line)
    if not match or not OPTION_MARKER.search(line):
        return text

    number, rest = match.groups()
    answer = "未在原文中识别到"
    explanation = "未在原文中识别到"

    answer_match = re.search(r"(?:答案|参考答案)[:：]\s*([A-E])", rest)
    if answer_match:
        answer = answer_match.group(1)
        rest = rest[: answer_match.start()].rstrip() + " " + rest[answer_match.end() :].lstrip()

    explanation_match = re.search(r"(?:解析|解释)[:：]\s*(.+)$", rest)
    if explanation_match:
        explanation = explanation_match.group(1).strip()
        rest = rest[: explanation_match.start()].rstrip()

    option_matches = list(OPTION_MARKER.finditer(rest))
    if not option_matches:
        return text

    stem = rest[: option_matches[0].start()].strip()
    options: list[str] = []
    for index, option_match in enumerate(option_matches):
        option_label = option_match.group(1)
        start = option_match.end()
        end = option_matches[index + 1].start() if index + 1 < len(option_matches) else len(rest)
        option_text = rest[start:end].strip()
        options.append(f"{option_label}. {option_text}")

    option_block = "\n".join(options)
    return (
        f"## 第 {number} 题\n"
        f"【题型】未在原文中识别到\n"
        f"【题干】{stem}\n"
        f"【选项】\n{option_block}\n"
        f"【答案】{answer}\n"
        f"【解析】{explanation}"
    )


def quality_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text):
            warnings.append(f"Suspicious OCR artifact remains: `{pattern}`")

    if OPTION_MARKER.search(text) and "【选项】" not in text and QUESTION_MARKER.search(text):
        warnings.append("Question-like text may still have merged options.")

    if re.search(r"\b(?:身份证|手机号|电话|住院号|门诊号|病历号)[:：]?\s*[\w-]{4,}", text):
        warnings.append("Possible sensitive patient identifier remains; de-identify before public sharing.")

    return warnings


def postprocess_text(text: str, include_warnings: bool = True) -> PostprocessResult:
    text = normalize_biomedical_notation(text)
    text = standardize_units(text)
    text = recover_question_structure(text)
    warnings = quality_warnings(text)
    if include_warnings and warnings:
        warning_lines = "\n".join(f"- {warning}" for warning in warnings)
        text = f"{text.rstrip()}\n\n---\n\n## OCR质量检查警告\n\n{warning_lines}\n"
    return PostprocessResult(text=text, warnings=warnings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Post-process medical OCR text.")
    parser.add_argument("input", nargs="?", help="Input text file. Reads stdin when omitted.")
    parser.add_argument("-o", "--output", help="Output text file. Writes stdout when omitted.")
    parser.add_argument("--no-warnings", action="store_true", help="Do not append QA warnings to output text.")
    args = parser.parse_args(argv)

    if args.input:
        source = Path(args.input).read_text(encoding="utf-8")
    else:
        source = sys.stdin.read()

    result = postprocess_text(source, include_warnings=not args.no_warnings)

    if args.output:
        Path(args.output).write_text(result.text, encoding="utf-8")
    else:
        sys.stdout.write(result.text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
