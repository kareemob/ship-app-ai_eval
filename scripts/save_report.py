import json
from pathlib import Path

REPORTS_FOLDER = Path("reports")


def _pretty(text):
    try:
        return json.dumps(json.loads(text), indent=2, ensure_ascii=False)
    except (TypeError, ValueError):
        return text or ""


def save_report(test_name, golden, answer, items, result, failure=None):
    REPORTS_FOLDER.mkdir(exist_ok=True)

    lines = [
        f"# {result}: {golden.name}",
        "",
        f"**Test:** {test_name}",
        "",
        f"**Question:** {golden.input}",
        "",
    ]

    if failure:
        lines += ["## Why it failed", "", failure, ""]

    lines += ["## Answer", "", answer, ""]

    for number, item in enumerate(items, start=1):
        if hasattr(item, "content"):
            lines += [
                "---",
                "",
                f"## Chunk [{number}]",
                "",
                f"`{item.source}` | score {item.score:.4f}",
                "",
                item.content.replace("\r\n", "\n"),
                "",
            ]
        else:
            lines += [
                "---",
                "",
                f"## Tool call [{number}]: {item.name}",
                "",
                "**Arguments**",
                "",
                "```json",
                json.dumps(item.args, indent=2, ensure_ascii=False),
                "```",
                "",
                "**Result**",
                "",
                "```json",
                _pretty(item.result),
                "```",
                "",
            ]

    for old_report in REPORTS_FOLDER.glob(f"*_{test_name}_{golden.name}.md"):
        old_report.unlink()

    report_file = REPORTS_FOLDER / f"{result}_{test_name}_{golden.name}.md"
    report_file.write_text("\n".join(lines), encoding="utf-8")