from medical_corrector import correct_biomedical_notation, quality_warnings


def main() -> None:
    source = (
        "患者SpO2下降，PaCO2升高，HCO3-代偿性升高。"
        "甲状腺功能提示T3、T4升高。肺功能FEV1/FVC下降。"
        "血糖控制指标HbA1c升高。血钙Ca2+异常。"
    )
    expected = (
        "患者SpO₂下降，PaCO₂升高，HCO₃⁻代偿性升高。"
        "甲状腺功能提示T₃、T₄升高。肺功能FEV₁/FVC下降。"
        "血糖控制指标HbA₁c升高。血钙Ca²⁺异常。"
    )
    actual = correct_biomedical_notation(source)
    assert actual == expected, f"\nexpected: {expected}\nactual:   {actual}"
    assert not quality_warnings(actual)
    print("medical_corrector smoke test passed")


if __name__ == "__main__":
    main()

