# Contributing / 贡献指南

欢迎提交 issue 和 PR。  
Issues and pull requests are welcome.

## 中文说明

欢迎通过 GitHub issue 反馈问题、提出改进建议或补充医学 OCR 场景。也欢迎提交 PR 改进 `SKILL.md`、`references/` 或 `scripts/`。

修改以下内容后，请运行本地验证：

- `skills/medical-ocr-router/SKILL.md`
- `skills/medical-ocr-router/references/`
- `skills/medical-ocr-router/scripts/`

提交 PR 前运行：

```powershell
python skills\medical-ocr-router\scripts\test_medical_corrector.py
python C:\Users\16648\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\medical-ocr-router
```

请不要在 issue、PR 或测试文件中加入患者隐私、真实病历、身份证号、手机号、医院号或检查报告原图。

## English

Please use GitHub issues for bugs, suggestions, and new medical OCR scenarios. Pull requests are welcome for improvements to `SKILL.md`, `references/`, and `scripts/`.

After modifying any of the following, run local validation:

- `skills/medical-ocr-router/SKILL.md`
- `skills/medical-ocr-router/references/`
- `skills/medical-ocr-router/scripts/`

Before opening a PR, run:

```powershell
python skills\medical-ocr-router\scripts\test_medical_corrector.py
python C:\Users\16648\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\medical-ocr-router
```

Do not include patient privacy data, real medical records, ID numbers, phone numbers, hospital IDs, or original examination report images in issues, PRs, or test files.

