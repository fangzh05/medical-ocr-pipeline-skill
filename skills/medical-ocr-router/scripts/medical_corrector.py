from __future__ import annotations

import re


DIRECT_REPLACEMENTS = {
    "PaCO2": "PaCO₂",
    "PaO2": "PaO₂",
    "PvCO2": "PvCO₂",
    "PvO2": "PvO₂",
    "PACO2": "PACO₂",
    "PAO2": "PAO₂",
    "SpO2": "SpO₂",
    "SaO2": "SaO₂",
    "SvO2": "SvO₂",
    "EtCO2": "EtCO₂",
    "PETCO2": "PETCO₂",
    "FiO2": "FiO₂",
    "HCO3-": "HCO₃⁻",
    "Na+": "Na⁺",
    "K+": "K⁺",
    "Cl-": "Cl⁻",
    "Ca2+": "Ca²⁺",
    "Mg2+": "Mg²⁺",
    "Fe2+": "Fe²⁺",
    "Fe3+": "Fe³⁺",
    "H+": "H⁺",
    "OH-": "OH⁻",
    "FEV1": "FEV₁",
    "HbA1c": "HbA₁c",
    "HbA1C": "HbA₁c",
    "CD4+": "CD4⁺",
    "CD8+": "CD8⁺",
    "CD20+": "CD20⁺",
    "FT3": "FT₃",
    "FT4": "FT₄",
    "rT3": "rT₃",
    "99mTc": "⁹⁹ᵐTc",
    "131I": "¹³¹I",
    "123I": "¹²³I",
    "18F-FDG": "¹⁸F-FDG",
    "67Ga": "⁶⁷Ga",
    "201Tl": "²⁰¹Tl",
}

SUSPICIOUS_TERMS = [
    "CO2",
    "O2",
    "PO2",
    "PCO2",
    "PaCO2",
    "PaO2",
    "SpO2",
    "SaO2",
    "HCO3",
    "Na+",
    "K+",
    "Ca2+",
    "Mg2+",
    "Cl-",
    "T3",
    "T4",
    "FT3",
    "FT4",
    "FEV1",
    "HbA1c",
    "CD4+",
    "CD8+",
    "beta2",
    "alpha1",
]

TOKEN_LEFT = r"(?<![A-Za-z0-9])"
TOKEN_RIGHT = r"(?![A-Za-z0-9])"


def _has_context(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def correct_biomedical_notation(text: str) -> str:
    """Correct common OCR-flattened biomedical notation conservatively."""
    for source, target in DIRECT_REPLACEMENTS.items():
        text = text.replace(source, target)

    text = re.sub(r"\bTNF-a\b", "TNF-α", text)
    text = re.sub(r"\bTNF-alpha\b", "TNF-α", text, flags=re.IGNORECASE)
    text = re.sub(r"\bIFN-gamma\b", "IFN-γ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bTGF-beta\b", "TGF-β", text, flags=re.IGNORECASE)

    thyroid_context = _has_context(
        text,
        r"甲状腺|甲亢|甲减|Graves|桥本|TSH|FT₃|FT₄|thyroid|hyperthyroidism|hypothyroidism",
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

    receptor_context = _has_context(text, r"受体|receptor|adrenergic|肾上腺素")
    if receptor_context:
        text = re.sub(r"\balpha1\b", "α₁", text, flags=re.IGNORECASE)
        text = re.sub(r"\balpha2\b", "α₂", text, flags=re.IGNORECASE)
        text = re.sub(r"\bbeta1\b", "β₁", text, flags=re.IGNORECASE)
        text = re.sub(r"\bbeta2\b", "β₂", text, flags=re.IGNORECASE)
        text = re.sub(r"\bβ1\b", "β₁", text)
        text = re.sub(r"\bβ2\b", "β₂", text)

    acid_base_context = _has_context(text, r"酸碱|血气|碳酸氢|bicarbonate|acidosis|alkalosis|ABG")
    if acid_base_context:
        text = re.sub(TOKEN_LEFT + r"HCO3" + TOKEN_RIGHT, "HCO₃⁻", text)

    return text


def quality_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    for term in SUSPICIOUS_TERMS:
        if term in text:
            warnings.append(f"Suspicious flattened biomedical notation remains: {term}")
    return warnings


def correction_report(text: str) -> str:
    corrected = correct_biomedical_notation(text)
    warnings = quality_warnings(corrected)
    if not warnings:
        return corrected
    warning_lines = "\n".join(f"- {warning}" for warning in warnings)
    return f"{corrected}\n\n---\n\n## OCR质量检查警告\n\n{warning_lines}\n"


if __name__ == "__main__":
    import sys

    source = sys.stdin.read()
    sys.stdout.write(correction_report(source))
