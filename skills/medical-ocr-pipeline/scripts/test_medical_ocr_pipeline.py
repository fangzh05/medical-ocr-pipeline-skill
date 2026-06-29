from __future__ import annotations

from medical_ocr_pipeline import OCRBlock, build_outputs, refine_blocks
from medical_symbol_corrector import correct_medical_symbols
from ocr_risk_detector import detect_block_risks, detect_text_risks
from question_structure_rebuilder import detect_question_number_gaps, rebuild_question_markdown


def assert_correct(source: str, expected: str) -> None:
    actual = correct_medical_symbols(source).text
    assert actual == expected, f"\nsource:   {source}\nexpected: {expected}\nactual:   {actual}"


def test_medical_symbol_correction_examples() -> None:
    cases = [
        ("患者SpO2下降，PaCO2升高，HCO3-代偿性升高。", "患者SpO₂下降，PaCO₂升高，HCO₃⁻代偿性升高。"),
        ("PaO2为60mmHg，FiO2为40%。", "PaO₂为60mmHg，FiO₂为40%。"),
        ("CO2潴留时应控制O2吸入浓度。", "CO₂潴留时应控制O₂吸入浓度。"),
        ("PETCO2持续升高提示通气不足。", "PETCO₂持续升高提示通气不足。"),
        ("FEV1/FVC下降提示阻塞性通气功能障碍。", "FEV₁/FVC下降提示阻塞性通气功能障碍。"),
        ("甲亢患者T3/T4升高，TSH降低。", "甲亢患者T₃/T₄升高，TSH降低。"),
        ("肿瘤T3期不能被纠正为T₃。", "肿瘤T3期不能被纠正为T₃。"),
        ("99mTc-MIBI用于甲状旁腺显像。", "⁹⁹ᵐTc-MIBI用于甲状旁腺显像。"),
        ("99rnTc疑似99mTc OCR错误。", "⁹⁹ᵐTc疑似⁹⁹ᵐTc OCR错误。"),
        ("131I治疗甲亢。", "¹³¹I治疗甲亢。"),
        ("I131应规范为¹³¹I。", "¹³¹I应规范为¹³¹I。"),
        ("18F-FDG PET/CT用于肿瘤代谢显像。", "¹⁸F-FDG PET/CT用于肿瘤代谢显像。"),
        ("Ca2+升高可见于甲旁亢。", "Ca²⁺升高可见于甲旁亢。"),
        ("Mg2+降低可导致心律失常。", "Mg²⁺降低可导致心律失常。"),
        ("Na+、K+、Cl-为常见电解质。", "Na⁺、K⁺、Cl⁻为常见电解质。"),
        ("H+浓度变化影响pH。", "H⁺浓度变化影响pH。"),
        ("cmH2O用于气道压力。", "cmH₂O用于气道压力。"),
        ("mg/kg用于麻醉药剂量。", "mg/kg用于麻醉药剂量。"),
        ("ug/kg应提示可能为μg/kg。", "μg/kg应提示可能为μg/kg。"),
        ("β2受体激动剂可舒张支气管。", "β₂受体激动剂可舒张支气管。"),
        ("α1受体兴奋可收缩血管。", "α₁受体兴奋可收缩血管。"),
        ("CD4+ T细胞减少见于免疫缺陷。", "CD4⁺ T细胞减少见于免疫缺陷。"),
        ("CD8+ T细胞升高。", "CD8⁺ T细胞升高。"),
        ("TNF-a应规范为TNF-α。", "TNF-α应规范为TNF-α。"),
        ("IFN-gamma应规范为IFN-γ。", "IFN-γ应规范为IFN-γ。"),
        ("TGF-beta参与纤维化。", "TGF-β参与纤维化。"),
        ("HCO3在血气分析中升高。", "HCO₃⁻在血气分析中升高。"),
        ("FT3和FT4升高。", "FT₃和FT₄升高。"),
        ("EtCO2升高见于通气不足。", "EtCO₂升高见于通气不足。"),
        ("SaO2降低提示低氧血症。", "SaO₂降低提示低氧血症。"),
    ]
    assert len(cases) >= 30
    for source, expected in cases:
        assert_correct(source, expected)


def test_risk_detector_examples() -> None:
    risks = detect_text_risks("99rnTc疑似99mTc OCR错误，ug/kg应提示可能为μg/kg。")
    tokens = {risk.token for risk in risks}
    assert "99rnTc" in tokens
    assert "99mTc" in tokens
    assert any(risk.suggestion == "μg/kg" for risk in risks)


def test_question_rebuilder_examples() -> None:
    text = "1. 下列哪项正确 A. 选项一 B. 选项二 C. 选项三 答案：C 解析：..."
    result = rebuild_question_markdown(text)
    assert "## 第 1 题" in result.markdown
    assert "A. 选项一" in result.markdown
    assert "B. 选项二" in result.markdown
    assert "C. 选项三" in result.markdown
    assert "【答案】\nC" in result.markdown
    assert result.warnings

    gaps = detect_question_number_gaps("第1题 内容\n第2题 内容\n第4题 内容")
    assert gaps == ["题号可能跳号: 第2题 后出现 第4题"]


def test_mock_pipeline_without_paddleocr() -> None:
    blocks = [
        OCRBlock(bbox=[[0, 0], [80, 0], [80, 20], [0, 20]], text="患者SpO2下降，PaCO2升高，HCO3-代偿性升高。", confidence=0.92),
        OCRBlock(bbox=[[0, 20], [80, 20], [80, 40], [0, 40]], text="99rnTc疑似99mTc OCR错误。", confidence=0.70),
        OCRBlock(bbox=[[0, 40], [80, 40], [80, 60], [0, 60]], text="1. 题干 A. 选项一 B. 选项二 C. 选项三 答案：C 解析：...", confidence=0.91),
    ]
    refined = refine_blocks(blocks, confidence_threshold=0.85)
    result = build_outputs(refined)
    assert "SpO₂" in result.final_markdown
    assert "PaCO₂" in result.final_markdown
    assert "⁹⁹ᵐTc" in result.final_markdown
    assert result.risks
    assert result.qa_warnings

    block_risks = detect_block_risks([block.to_dict() for block in blocks], confidence_threshold=0.85)
    assert any(risk.risk_type == "low_confidence" for risk in block_risks)


def main() -> None:
    test_medical_symbol_correction_examples()
    test_risk_detector_examples()
    test_question_rebuilder_examples()
    test_mock_pipeline_without_paddleocr()
    print("medical OCR pipeline mock tests passed")


if __name__ == "__main__":
    main()

