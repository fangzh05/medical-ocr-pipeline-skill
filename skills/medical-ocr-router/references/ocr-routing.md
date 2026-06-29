# OCR Source Text Intake Notes

This skill is a medical OCR post-processing and QA skill. It should usually start from existing OCR text, not from OCR engine selection.

Use this reference only when the OCR source text is too broken to correct.

## When to Ask for Better OCR Input

Ask the user for a better OCR source, page image, or re-run only when:

- whole lines are missing
- option labels are not visible
- formulas are unreadable
- table columns cannot be distinguished
- too many words are marked uncertain
- the text appears to come from the wrong page or language

## What to Preserve Before Post-Processing

When receiving OCR text, preserve:

- page number markers
- heading hierarchy
- question numbers
- option labels such as `A.`、`B.`、`C.`、`D.`
- answer and explanation markers
- table row boundaries when visible
- uncertain spans from the OCR stage

## Main Boundary

Do not turn a post-processing task into a tool-selection discussion. Only mention OCR reruns when the text quality prevents safe correction.

