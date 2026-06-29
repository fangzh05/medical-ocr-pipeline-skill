# Biomedical Notation Reference

## Common Correct Forms

- PaCO₂, PaO₂, PvCO₂, PvO₂
- SpO₂, SaO₂, SvO₂, FiO₂, EtCO₂, PETCO₂
- HCO₃⁻, CO₂, O₂
- Na⁺, K⁺, Cl⁻, Ca²⁺, Mg²⁺, Fe²⁺, Fe³⁺, H⁺, OH⁻
- T₃, T₄, FT₃, FT₄, rT₃
- FEV₁/FVC
- HbA₁c
- CD4⁺, CD8⁺, CD20⁺
- TNF-α, IFN-γ, TGF-β, IL-1β, IL-6
- α₁ receptor, α₂ receptor, β₁ receptor, β₂ receptor
- ⁹⁹ᵐTc, ¹³¹I, ¹²³I, ¹⁸F-FDG, ⁶⁷Ga, ²⁰¹Tl

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

