# OCR Routing Reference

## Input Inspection

For PDFs:

- Extract embedded text first.
- Check whether extracted text preserves notation such as PaCO₂, HCO₃⁻, SpO₂, T₃, Ca²⁺, HbA₁c, and FEV₁/FVC.
- If embedded text is incomplete, corrupted, or notation-flattened, render pages to images at 300-400 DPI and use image OCR.
- For mixed pages, run layout analysis before recognition.

For images:

- Check resolution, contrast, rotation, margins, blur, and text density.
- Deskew tilted scans.
- Upscale small screenshots by 2x or 3x when thin subscripts or superscripts are at risk.
- Avoid aggressive binarization if it damages minus signs, plus signs, Greek letters, or small characters.

## Region Routing

Use standard OCR for normal paragraphs and list text.

Use formula-aware recognition for:

- equations
- superscripts or subscripts
- ions and charges
- chemical notation
- physiological gases and acid-base notation
- Greek letters
- isotope notation

Use table recognition for tabular material. Output simple tables as Markdown. Use HTML tables when merged cells or complex layout would be damaged by Markdown.

Use document layout parsing for mixed textbook pages, slides, PDFs, and screenshots with titles, columns, figures, captions, tables, and formulas.

## Question Banks

Preserve:

- question number
- question type
- stem
- each option
- answer when present
- explanation when present

Never merge choices into the question stem. If answer or explanation is not visible, mark it as not recognized from the source.

## Error Handling

If formula recognition is unavailable, run standard OCR on the formula-sensitive region, apply biomedical correction, and mark the region for review.

If table recognition is unavailable, reconstruct the table only when row and column structure is clear. Otherwise preserve aligned text and mark the table for review.

If layout parsing is unavailable, split regions using OCR boxes or image processing heuristics, preserve reading order, and mark low-confidence regions.

