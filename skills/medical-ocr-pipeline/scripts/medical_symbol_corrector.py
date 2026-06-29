from __future__ import annotations

import re
from dataclasses import dataclass, field


TOKEN_LEFT = r"(?<![A-Za-z0-9])"
TOKEN_RIGHT = r"(?![A-Za-z0-9])"


@dataclass
class CorrectionResult:
    text: str
    warnings: list[str] = field(default_factory=list)


def _replace_token(text: str, source: str, target: str) -> str:
    return re.sub(TOKEN_LEFT + re.escape(source) + TOKEN_RIGHT, target, text)


def _has_context(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _warn(warnings: list[str], message: str) -> None:
    if message not in warnings:
        warnings.append(message)


def correct_medical_symbols(text: str) -> CorrectionResult:
    warnings: list[str] = []
    corrected = text

    direct = {
        "PaCO2": "PaCO₂",
        "PaO2": "PaO₂",
        "SpO2": "SpO₂",
        "SaO2": "SaO₂",
        "EtCO2": "EtCO₂",
        "PETCO2": "PETCO₂",
        "FiO2": "FiO₂",
        "FEV1/FVC": "FEV₁/FVC",
        "FEV1": "FEV₁",
        "FT3": "FT₃",
        "FT4": "FT₄",
        "HCO3-": "HCO₃⁻",
        "HCO3−": "HCO₃⁻",
        "Ca2+": "Ca²⁺",
        "Mg2+": "Mg²⁺",
        "Na+": "Na⁺",
        "K+": "K⁺",
        "Cl-": "Cl⁻",
        "Cl−": "Cl⁻",
        "H+": "H⁺",
        "OH-": "OH⁻",
        "OH−": "OH⁻",
        "CD4+": "CD4⁺",
        "CD8+": "CD8⁺",
        "99mTc": "⁹⁹ᵐTc",
        "131I": "¹³¹I",
        "I131": "¹³¹I",
        "18F-FDG": "¹⁸F-FDG",
    }

    for source, target in sorted(direct.items(), key=lambda item: len(item[0]), reverse=True):
        corrected = _replace_token(corrected, source, target)

    if re.search(TOKEN_LEFT + r"99rnTc" + TOKEN_RIGHT, corrected):
        corrected = re.sub(TOKEN_LEFT + r"99rnTc" + TOKEN_RIGHT, "⁹⁹ᵐTc", corrected)
        _warn(warnings, "99rnTc may be OCR confusion for 99mTc; normalized to ⁹⁹ᵐTc.")

    corrected = re.sub(TOKEN_LEFT + r"TNF-a" + TOKEN_RIGHT, "TNF-α", corrected)
    corrected = re.sub(TOKEN_LEFT + r"TNF-alpha" + TOKEN_RIGHT, "TNF-α", corrected, flags=re.IGNORECASE)
    corrected = re.sub(TOKEN_LEFT + r"IFN-gamma" + TOKEN_RIGHT, "IFN-γ", corrected, flags=re.IGNORECASE)
    corrected = re.sub(TOKEN_LEFT + r"TGF-beta" + TOKEN_RIGHT, "TGF-β", corrected, flags=re.IGNORECASE)

    receptor_context = _has_context(corrected, r"受体|receptor|激动剂|拮抗剂|肾上腺素")
    if receptor_context:
        receptor_replacements = {
            "β2": "β₂",
            "β1": "β₁",
            "α1": "α₁",
            "α2": "α₂",
            "beta2": "β₂",
            "beta1": "β₁",
            "alpha1": "α₁",
            "alpha2": "α₂",
        }
        for source, target in receptor_replacements.items():
            corrected = _replace_token(corrected, source, target)

    acid_base_context = _has_context(corrected, r"血气|酸碱|碳酸氢|呼吸|通气|酸中毒|碱中毒|bicarbonate|ABG|肺")
    if acid_base_context:
        corrected = re.sub(TOKEN_LEFT + r"HCO3" + TOKEN_RIGHT, "HCO₃⁻", corrected)

    respiratory_context = _has_context(corrected, r"呼吸|通气|氧|给氧|吸入|潴留|麻醉|肺|ventilation|oxygen|CO₂|O₂")
    if respiratory_context:
        corrected = re.sub(TOKEN_LEFT + r"CO2" + TOKEN_RIGHT, "CO₂", corrected)
        corrected = re.sub(TOKEN_LEFT + r"O2" + TOKEN_RIGHT, "O₂", corrected)
        corrected = re.sub(r"cmH2O", "cmH₂O", corrected)

    thyroid_context = _has_context(corrected, r"甲状腺|甲亢|甲减|Graves|TSH|内分泌|thyroid|hyperthyroidism|hypothyroidism")
    tumor_context = _has_context(corrected, r"肿瘤|分期|TNM|癌|期")
    if thyroid_context and not tumor_context:
        corrected = re.sub(TOKEN_LEFT + r"T3/T4" + TOKEN_RIGHT, "T₃/T₄", corrected)
        corrected = re.sub(TOKEN_LEFT + r"T3" + TOKEN_RIGHT, "T₃", corrected)
        corrected = re.sub(TOKEN_LEFT + r"T4" + TOKEN_RIGHT, "T₄", corrected)
    elif re.search(TOKEN_LEFT + r"T[34]" + TOKEN_RIGHT, corrected):
        _warn(warnings, "T3/T4-like token kept because context may be staging, question numbering, or non-thyroid text.")

    if re.search(TOKEN_LEFT + r"ug\s*/\s*kg" + TOKEN_RIGHT, corrected, flags=re.IGNORECASE):
        corrected = re.sub(TOKEN_LEFT + r"ug\s*/\s*kg" + TOKEN_RIGHT, "μg/kg", corrected, flags=re.IGNORECASE)
        _warn(warnings, "ug/kg normalized to μg/kg; verify micro symbol in source.")

    unit_replacements = [
        (TOKEN_LEFT + r"mm\s+Hg" + TOKEN_RIGHT, "mmHg"),
        (TOKEN_LEFT + r"mmol\s*/\s*L" + TOKEN_RIGHT, "mmol/L"),
        (TOKEN_LEFT + r"mEq\s*/\s*L" + TOKEN_RIGHT, "mEq/L"),
        (TOKEN_LEFT + r"mg\s*/\s*kg" + TOKEN_RIGHT, "mg/kg"),
        (TOKEN_LEFT + r"mg\s*/\s*dL" + TOKEN_RIGHT, "mg/dL"),
        (TOKEN_LEFT + r"mcg\s*/\s*kg" + TOKEN_RIGHT, "μg/kg"),
        (TOKEN_LEFT + r"mcg\s*/\s*L" + TOKEN_RIGHT, "μg/L"),
        (TOKEN_LEFT + r"ug\s*/\s*L" + TOKEN_RIGHT, "μg/L"),
        (TOKEN_LEFT + r"cmH2O" + TOKEN_RIGHT, "cmH₂O"),
        (r"℃", "°C"),
    ]
    for pattern, replacement in unit_replacements:
        corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)

    corrected = re.sub(
        r"\b(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(mmHg|mmol/L|mEq/L|mg/kg|μg/kg|mg/dL|μg/L|cmH₂O)\b",
        r"\1-\2 \3",
        corrected,
    )

    return CorrectionResult(text=corrected, warnings=warnings)


def correct_text(text: str) -> str:
    return correct_medical_symbols(text).text
