# Question Bank OCR Example / 题库 OCR 示例

## Raw OCR

```text
1. 下列哪项提示呼吸衰竭 A. PaCO2升高 B. SpO2下降 C. HbA1c升高 D. TSH降低 答案:B 解析:低氧血症常见
```

## Risk Detection

- `PaCO2`: blood gas notation risk
- `SpO2`: oxygen saturation notation risk
- `HbA1c`: diabetes marker notation risk
- Options appear merged into the question stem

## Refined OCR

```text
## 第 1 题
【题型】
未在原文中识别到
【题干】
下列哪项提示呼吸衰竭
【选项】
A. PaCO₂升高
B. SpO₂下降
C. HbA₁c升高
D. TSH降低
【答案】
B
【解析】
低氧血症常见
【OCR复核】
- 选项可能曾被 OCR 合并到同一行，已按选项标记拆分
```

## QA Warnings

- Verify that all expected options are present.
- Do not invent missing answer or explanation text.

