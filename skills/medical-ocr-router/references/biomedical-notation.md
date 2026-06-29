# Biomedical Notation Reference

Use this reference when reviewing or extending medical OCR correction rules.

## Common Correct Forms

- Blood gas and oxygenation: PaCO₂, PaO₂, PvCO₂, PvO₂, SpO₂, SaO₂, SvO₂, ScvO₂, FiO₂, EtCO₂, PETCO₂
- Acid-base and chemistry: HCO₃⁻, CO₂, O₂, H⁺, OH⁻
- Electrolytes and ions: Na⁺, K⁺, Cl⁻, Ca²⁺, Mg²⁺, Fe²⁺, Fe³⁺
- Thyroid: T₃, T₄, FT₃, FT₄, rT₃
- Pulmonary function: FEV₁, FEV₁/FVC
- Metabolism: HbA₁c
- Immunology: CD4⁺, CD8⁺, CD20⁺, TNF-α, IFN-γ, TGF-β, IL-1β, IL-6
- Receptors: α₁ receptor, α₂ receptor, β₁ receptor, β₂ receptor
- Nuclear medicine: ⁹⁹ᵐTc, ¹³¹I, ¹²³I, ¹⁸F-FDG, ⁶⁷Ga, ²⁰¹Tl

## OCR Flattened Form Mapping

| Flattened OCR | Correct notation |
|---|---|
| PaCO2 | PaCO₂ |
| PaO2 | PaO₂ |
| SaO2 | SaO₂ |
| SpO2 | SpO₂ |
| HCO3- | HCO₃⁻ |
| Na+ | Na⁺ |
| K+ | K⁺ |
| Cl- | Cl⁻ |
| Ca2+ | Ca²⁺ |
| Mg2+ | Mg²⁺ |
| FEV1/FVC | FEV₁/FVC |
| HbA1c | HbA₁c |
| T3/T4 | T₃/T₄ |
| CD4+ | CD4⁺ |
| CD8+ | CD8⁺ |
| TNF-a | TNF-α |
| IFN-gamma | IFN-γ |
| 131I | ¹³¹I |
| 99mTc | ⁹⁹ᵐTc |

## Suspicious Flattened Forms

Search final OCR output for:

```text
CO2
O2
PO2
PCO2
PaCO2
PaO2
SpO2
SaO2
HCO3
Na+
K+
Ca2+
Mg2+
Cl-
T3
T4
FT3
FT4
FEV1
HbA1c
CD4+
CD8+
beta2
alpha1
99mTc
131I
```

Inspect context before correcting. Do not blindly replace every occurrence.

## Conservative Exceptions

Do not auto-correct when the number is clearly not a subscript or superscript:

- 第2章
- 2024年
- 表3
- 选项A2
- 病例2
- T3期肿瘤, unless the source clearly means thyroid hormone T₃

