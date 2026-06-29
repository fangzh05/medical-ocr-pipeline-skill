# Anesthesia Monitoring OCR Example / 麻醉监测 OCR 示例

## Raw OCR

```text
PETCO2持续升高提示通气不足。EtCO2升高见于低通气。气道压力20cmH2O。芬太尼2ug/kg。
```

## Risk Detection

- `PETCO2`: end-tidal CO₂ notation risk
- `EtCO2`: end-tidal CO₂ notation risk
- `cmH2O`: unit subscript risk
- `ug/kg`: microgram unit symbol risk

## Refined OCR

```text
PETCO₂持续升高提示通气不足。EtCO₂升高见于低通气。气道压力20cmH₂O。芬太尼2μg/kg。
```

## QA Warnings

- `ug/kg` was normalized to `μg/kg`; verify the micro symbol and dose from the source.
- Airway pressure unit was normalized to `cmH₂O`.

