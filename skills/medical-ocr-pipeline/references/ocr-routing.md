# Medical OCR Pipeline Reference

This skill is a medical OCR refinement pipeline, not a plain OCR post-processor. Use this reference when implementing or reviewing the OCR stage.

## Pipeline Stages

1. Load a page image from an image path or a page rendered from PDF.
2. Optionally preprocess the image: deskew, crop margins, normalize contrast.
3. Run initial OCR and preserve each block:

```json
{
  "bbox": [[0, 0], [100, 0], [100, 20], [0, 20]],
  "text": "PaCO2",
  "confidence": 0.93
}
```

4. Detect low-confidence blocks and high-risk medical tokens.
5. Crop high-risk bboxes and create debug images.
6. Enhance crop regions with moderate 2x/3x enlargement, sharpening, contrast, grayscale, and optional binarization.
7. Re-run OCR on each crop.
8. Compare initial and crop OCR.
9. Apply context-aware medical symbol correction.
10. Rebuild textbook, table, paragraph, or question-bank structure.
11. Emit Markdown, JSON, crop debug files, and QA report.

## Boundary

The pipeline can improve reliability through local re-recognition and validation, but it cannot modify PaddleOCR model weights or guarantee perfect OCR.

When a token cannot be confirmed, mark it as `[需人工复核: ...]`.

