from postprocess_medical_ocr import (
    normalize_biomedical_notation,
    postprocess_text,
    quality_warnings,
    standardize_units,
)


def test_symbol_corrections() -> None:
    cases = [
        ("PaCO2升高", "PaCO₂升高"),
        ("PaO2下降", "PaO₂下降"),
        ("SaO2/SpO2降低", "SaO₂/SpO₂降低"),
        ("HCO3-代偿性升高", "HCO₃⁻代偿性升高"),
        ("HCO3−降低", "HCO₃⁻降低"),
        ("FEV1/FVC下降", "FEV₁/FVC下降"),
        ("FEV1占预计值百分比", "FEV₁占预计值百分比"),
        ("HbA1c升高", "HbA₁c升高"),
        ("血清Na+降低", "血清Na⁺降低"),
        ("K+升高", "K⁺升高"),
        ("Cl-降低", "Cl⁻降低"),
        ("Ca2+异常", "Ca²⁺异常"),
        ("Mg2+降低", "Mg²⁺降低"),
        ("Fe3+参与反应", "Fe³⁺参与反应"),
        ("CD4+ T细胞减少", "CD4⁺ T细胞减少"),
        ("CD8+ T细胞升高", "CD8⁺ T细胞升高"),
        ("TNF-a升高", "TNF-α升高"),
        ("IFN-gamma释放", "IFN-γ释放"),
        ("甲状腺功能提示T3/T4升高", "甲状腺功能提示T₃/T₄升高"),
        ("甲状腺功能提示T3、T4升高", "甲状腺功能提示T₃、T₄升高"),
        ("131I治疗甲亢", "¹³¹I治疗甲亢"),
        ("99mTc显像", "⁹⁹ᵐTc显像"),
        ("18F-FDG PET", "¹⁸F-FDG PET"),
        ("beta2 receptor激动剂", "β₂ receptor激动剂"),
    ]

    for source, expected in cases:
        actual = normalize_biomedical_notation(source)
        assert actual == expected, f"\nsource:   {source}\nexpected: {expected}\nactual:   {actual}"


def test_unit_standardization() -> None:
    cases = [
        ("PaCO₂ 35 - 45 mm Hg", "PaCO₂ 35-45 mmHg"),
        ("Na⁺ 135 - 145 mmol / L", "Na⁺ 135-145 mmol/L"),
        ("血糖 126 mg / dL", "血糖 126 mg/dL"),
        ("TSH 4.5 ug / L", "TSH 4.5 μg/L"),
    ]
    for source, expected in cases:
        actual = standardize_units(source)
        assert actual == expected, f"\nsource:   {source}\nexpected: {expected}\nactual:   {actual}"


def test_question_recovery() -> None:
    source = "1. 下列哪项提示呼吸衰竭 A. PaCO2升高 B. SpO2下降 C. HbA1c升高 D. TSH降低 答案:B 解析:低氧血症常见"
    expected = (
        "## 第 1 题\n"
        "【题型】未在原文中识别到\n"
        "【题干】下列哪项提示呼吸衰竭\n"
        "【选项】\n"
        "A. PaCO₂升高\n"
        "B. SpO₂下降\n"
        "C. HbA₁c升高\n"
        "D. TSH降低\n"
        "【答案】B\n"
        "【解析】低氧血症常见"
    )
    actual = postprocess_text(source, include_warnings=False).text
    assert actual == expected, f"\nexpected:\n{expected}\nactual:\n{actual}"


def test_quality_warnings_are_clear() -> None:
    warnings = quality_warnings("PaCO2 still flattened")
    assert warnings
    assert "PaCO2" in warnings[0]


def main() -> None:
    test_symbol_corrections()
    test_unit_standardization()
    test_question_recovery()
    test_quality_warnings_are_clear()
    print("medical OCR postprocessor tests passed")


if __name__ == "__main__":
    main()

