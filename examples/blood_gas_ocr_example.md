# Blood Gas OCR Example / 血气分析 OCR 示例

## Raw OCR

```text
患者SpO2下降，PaCO2升高，HCO3-代偿性升高。PaO2为60mmHg，FiO2为40%。CO2潴留时应控制O2吸入浓度。
```

## Risk Detection

- `SpO2`: medical subscript risk, suggest `SpO₂`
- `PaCO2`: blood gas notation risk, suggest `PaCO₂`
- `HCO3-`: bicarbonate notation risk, suggest `HCO₃⁻`
- `PaO2`: blood gas notation risk, suggest `PaO₂`
- `FiO2`: oxygen fraction notation risk, suggest `FiO₂`
- `CO2/O2`: respiratory context risk, suggest `CO₂/O₂`

## Refined OCR

```text
患者SpO₂下降，PaCO₂升高，HCO₃⁻代偿性升高。PaO₂为60mmHg，FiO₂为40%。CO₂潴留时应控制O₂吸入浓度。
```

## QA Warnings

- Verify blood gas values against the source image.
- If subscript shapes are unclear, crop and re-run OCR on the blood gas line.

