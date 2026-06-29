from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Risk:
    token: str
    risk_type: str
    suggestion: str
    confidence: str
    reason: str
    block_index: int | None = None
    bbox: Any | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "token": self.token,
            "risk_type": self.risk_type,
            "suggestion": self.suggestion,
            "confidence": self.confidence,
            "reason": self.reason,
            "block_index": self.block_index,
            "bbox": self.bbox,
        }


RISK_RULES = [
    (r"\bPaCO2\b", "medical_subscript", "PaCO₂", "high", "blood gas notation often requires CO₂ subscript"),
    (r"\bPaO2\b", "medical_subscript", "PaO₂", "high", "blood gas notation often requires O₂ subscript"),
    (r"\bSpO2\b", "medical_subscript", "SpO₂", "high", "oxygen saturation notation often requires O₂ subscript"),
    (r"\bSaO2\b", "medical_subscript", "SaO₂", "high", "oxygen saturation notation often requires O₂ subscript"),
    (r"\bEtCO2\b", "medical_subscript", "EtCO₂", "high", "end-tidal CO₂ notation"),
    (r"\bPETCO2\b", "medical_subscript", "PETCO₂", "high", "end-tidal CO₂ notation"),
    (r"\bHCO3-?\b", "medical_charge", "HCO₃⁻", "high", "bicarbonate may require subscript and negative charge"),
    (r"\bFEV1/FVC\b", "medical_subscript", "FEV₁/FVC", "high", "pulmonary function notation"),
    (r"\bFEV1\b", "medical_subscript", "FEV₁", "high", "pulmonary function notation"),
    (r"\bFT3\b", "medical_subscript", "FT₃", "medium", "thyroid hormone notation"),
    (r"\bFT4\b", "medical_subscript", "FT₄", "medium", "thyroid hormone notation"),
    (r"\b99rnTc\b", "ocr_confusion", "⁹⁹ᵐTc", "medium", "rn may be OCR confusion for m in nuclear medicine isotope notation"),
    (r"\b99mTc\b", "isotope_notation", "⁹⁹ᵐTc", "high", "nuclear medicine isotope notation"),
    (r"\b131I\b", "isotope_notation", "¹³¹I", "high", "iodine isotope notation"),
    (r"\bI131\b", "isotope_order", "¹³¹I", "medium", "I131 is often OCR/order variant of 131I"),
    (r"\b18F-FDG\b", "isotope_notation", "¹⁸F-FDG", "high", "PET tracer notation"),
    (r"\bCa2\+\b", "medical_charge", "Ca²⁺", "high", "ion charge notation"),
    (r"\bMg2\+\b", "medical_charge", "Mg²⁺", "high", "ion charge notation"),
    (r"\bNa\+\b", "medical_charge", "Na⁺", "medium", "ion charge notation"),
    (r"\bK\+\b", "medical_charge", "K⁺", "medium", "ion charge notation"),
    (r"\bCl-\b", "medical_charge", "Cl⁻", "medium", "ion charge notation"),
    (r"\bH\+\b", "medical_charge", "H⁺", "medium", "ion charge notation"),
    (r"\bcmH2O\b", "unit_subscript", "cmH₂O", "medium", "airway pressure unit often uses H₂O"),
    (r"\bug\s*/\s*kg\b", "unit_symbol", "μg/kg", "medium", "u may be OCR fallback for μ"),
    (r"℃", "unit_symbol", "°C", "low", "temperature symbol variant"),
    (r"\bSp0 2\b|\bSp02\b|\bSa02\b|\bPa02\b", "ocr_confusion", "O₂ notation", "medium", "0 may be OCR confusion for O"),
    (r"\bTNF-a\b", "greek_letter", "TNF-α", "high", "cytokine notation"),
    (r"\bIFN-gamma\b", "greek_letter", "IFN-γ", "high", "cytokine notation"),
    (r"\bTGF-beta\b", "greek_letter", "TGF-β", "high", "cytokine notation"),
]


def detect_text_risks(text: str, block_index: int | None = None, bbox: Any | None = None) -> list[Risk]:
    risks: list[Risk] = []
    for pattern, risk_type, suggestion, confidence, reason in RISK_RULES:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.ASCII):
            risks.append(
                Risk(
                    token=match.group(0),
                    risk_type=risk_type,
                    suggestion=suggestion,
                    confidence=confidence,
                    reason=reason,
                    block_index=block_index,
                    bbox=bbox,
                )
            )
    return risks


def detect_block_risks(blocks: list[dict[str, Any]], confidence_threshold: float = 0.85) -> list[Risk]:
    risks: list[Risk] = []
    for index, block in enumerate(blocks):
        text = str(block.get("text", ""))
        bbox = block.get("bbox")
        confidence = block.get("confidence")
        if confidence is not None and float(confidence) < confidence_threshold:
            risks.append(
                Risk(
                    token=text,
                    risk_type="low_confidence",
                    suggestion="[需人工复核]",
                    confidence="high",
                    reason=f"OCR confidence {confidence:.2f} is below threshold {confidence_threshold:.2f}",
                    block_index=index,
                    bbox=bbox,
                )
            )
        risks.extend(detect_text_risks(text, block_index=index, bbox=bbox))
    return risks
