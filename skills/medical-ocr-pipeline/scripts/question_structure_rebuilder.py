from __future__ import annotations

import re
from dataclasses import dataclass, field


OPTION_RE = re.compile(r"([A-E])\s*[.、．]\s*")
QUESTION_RE = re.compile(r"(?:^|\n)\s*(?:第\s*)?(\d{1,3})\s*(?:题|[.、．])\s*")


@dataclass
class QuestionResult:
    markdown: str
    warnings: list[str] = field(default_factory=list)


def detect_question_number_gaps(text: str) -> list[str]:
    numbers = [int(match.group(1)) for match in QUESTION_RE.finditer(text)]
    warnings: list[str] = []
    for left, right in zip(numbers, numbers[1:]):
        if right != left + 1:
            warnings.append(f"题号可能跳号: 第{left}题 后出现 第{right}题")
    return warnings


def _extract_answer(text: str) -> tuple[str, str]:
    match = re.search(r"(?:答案|参考答案)[:：]\s*([A-E]|正确|错误|对|错|.+?)(?=\s*(?:解析|$))", text)
    if not match:
        return "未在原文中识别到", text
    answer = match.group(1).strip()
    remaining = text[: match.start()].strip() + " " + text[match.end() :].strip()
    return answer, remaining.strip()


def _extract_explanation(text: str) -> tuple[str, str]:
    match = re.search(r"(?:解析|解释)[:：]\s*(.+)$", text)
    if not match:
        return "未在原文中识别到", text
    explanation = match.group(1).strip()
    remaining = text[: match.start()].strip()
    return explanation, remaining


def rebuild_question_markdown(text: str, default_type: str = "未在原文中识别到") -> QuestionResult:
    warnings = detect_question_number_gaps(text)
    one_line = " ".join(line.strip() for line in text.splitlines() if line.strip())

    q_match = re.match(r"(?:第\s*)?(\d{1,3})\s*(?:题|[.、．])\s*(.+)", one_line)
    if not q_match:
        return QuestionResult(markdown=text, warnings=warnings)

    number, rest = q_match.groups()
    answer, rest = _extract_answer(rest)
    explanation, rest = _extract_explanation(rest)

    option_matches = list(OPTION_RE.finditer(rest))
    if not option_matches:
        warnings.append("未识别到清晰选项结构")
        stem = rest.strip()
        options_block = "未在原文中识别到"
    else:
        stem = rest[: option_matches[0].start()].strip()
        options: list[str] = []
        seen_labels: list[str] = []
        for index, option_match in enumerate(option_matches):
            label = option_match.group(1)
            seen_labels.append(label)
            start = option_match.end()
            end = option_matches[index + 1].start() if index + 1 < len(option_matches) else len(rest)
            option_text = rest[start:end].strip()
            options.append(f"{label}. {option_text}")
        options_block = "\n".join(options)
        expected = ["A", "B", "C", "D"]
        missing = [label for label in expected if label not in seen_labels]
        if missing:
            warnings.append("选项可能缺失: " + ", ".join(missing))
        if len(option_matches) >= 2 and "\n" not in text:
            warnings.append("选项可能曾被 OCR 合并到同一行，已按选项标记拆分")

    review_lines = warnings or ["未发现明显题库结构风险"]
    review_block = "\n".join(f"- {warning}" for warning in review_lines)
    markdown = (
        f"## 第 {number} 题\n"
        f"【题型】\n{default_type}\n"
        f"【题干】\n{stem or '未在原文中识别到'}\n"
        f"【选项】\n{options_block}\n"
        f"【答案】\n{answer}\n"
        f"【解析】\n{explanation}\n"
        f"【OCR复核】\n{review_block}"
    )
    return QuestionResult(markdown=markdown, warnings=warnings)

