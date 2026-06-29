# Nuclear Medicine OCR Example / 核医学 OCR 示例

## Raw OCR

```text
99rnTc疑似99mTc OCR错误。131I治疗甲亢。I131应规范为131I。18F-FDG PET/CT用于肿瘤代谢显像。
```

## Risk Detection

- `99rnTc`: OCR confusion risk, `rn` may be mistaken for `m`
- `99mTc`: isotope notation risk
- `131I` / `I131`: iodine isotope notation risk
- `18F-FDG`: PET tracer notation risk

## Refined OCR

```text
⁹⁹ᵐTc疑似⁹⁹ᵐTc OCR错误。¹³¹I治疗甲亢。¹³¹I应规范为¹³¹I。¹⁸F-FDG PET/CT用于肿瘤代谢显像。
```

## QA Warnings

- `99rnTc` was normalized to `⁹⁹ᵐTc`; verify against the source image.
- Isotope notation should be manually checked when source text is small or blurry.

