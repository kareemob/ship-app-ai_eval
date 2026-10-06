from pathlib import Path

REPORTS_FOLDER = Path("reports")


def save_report(golden, answer, chunks, result, failure=None):
    REPORTS_FOLDER.mkdir(exist_ok=True)

    lines = [
        f"# {result}: {golden.name}",
        "",
        f"**Question:** {golden.input}",
        "",
    ]

    if failure:
        lines += ["## Why it failed", "", failure, ""]

    lines += ["## Answer", "", answer, ""]

    for number, chunk in enumerate(chunks, start=1):
        lines += [
            "---",
            "",
            f"## Chunk [{number}]",
            "",
            f"`{chunk.source}` | score {chunk.score:.4f}",
            "",
            chunk.content.replace("\r\n", "\n"),
            "",
        ]

    for old_report in REPORTS_FOLDER.glob(f"*_{golden.name}.md"):
        old_report.unlink()

    report_file = REPORTS_FOLDER / f"{result}_{golden.name}.md"
    report_file.write_text("\n".join(lines), encoding="utf-8")