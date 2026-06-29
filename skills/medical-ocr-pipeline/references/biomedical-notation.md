# Biomedical Notation Reference

Use this reference when extending medical risk detection, symbol correction, and QA warnings.

## Blood Gas And Respiratory

| OCR / Risk Form | Preferred Form | Context |
|---|---|---|
| PaCO2 | PaCO₂ | blood gas |
| PaO2 | PaO₂ | blood gas |
| SpO2 | SpO₂ | pulse oximetry |
| SaO2 | SaO₂ | arterial saturation |
| EtCO2 | EtCO₂ | anesthesia / ventilation |
| PETCO2 | PETCO₂ | end-tidal CO₂ |
| FiO2 | FiO₂ | oxygen fraction |
| HCO3- | HCO₃⁻ | bicarbonate |
| HCO3 | HCO₃⁻ | acid-base / blood gas context only |
| CO2潴留 | CO₂潴留 | respiratory context |
| O2吸入 | O₂吸入 | respiratory context |

## Pulmonary Function

- FEV1 -> FEV₁
- FEV1/FVC -> FEV₁/FVC

## Endocrine

- FT3 -> FT₃
- FT4 -> FT₄
- T3/T4 -> T₃/T₄ only in thyroid context

Do not convert tumor staging such as `肿瘤T3期`.

## Nuclear Medicine

- 99mTc -> ⁹⁹ᵐTc
- 99rnTc -> ⁹⁹ᵐTc with QA warning
- 131I -> ¹³¹I
- I131 -> ¹³¹I
- 18F-FDG -> ¹⁸F-FDG

## Electrolytes

- Ca2+ -> Ca²⁺
- Mg2+ -> Mg²⁺
- Na+ -> Na⁺
- K+ -> K⁺
- Cl- -> Cl⁻
- H+ -> H⁺
- OH- -> OH⁻

## Immunology And Receptors

- CD4+ -> CD4⁺
- CD8+ -> CD8⁺
- β2 receptor -> β₂ receptor
- β1 receptor -> β₁ receptor
- α1 receptor -> α₁ receptor
- α2 receptor -> α₂ receptor
- TNF-a -> TNF-α
- IFN-gamma -> IFN-γ
- TGF-beta -> TGF-β

## OCR Confusions

Flag these for review:

- O and 0
- l and 1
- I and 1
- μ and u
- ℃ and °C
- m and rn
- HCO3 and HCO₃
- 99mTc and 99rnTc
- cmH2O and cmH₂O
- ug/kg and μg/kg

