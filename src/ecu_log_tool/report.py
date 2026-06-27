"""
Markdown report generation for the ECU Log Pre-Analysis Tool.

The report gives a compact PASS/FAIL summary that can be attached to a
manual validation record or used as first pre-analysis evidence.
"""

from pathlib import Path


def _format_check_list(checks):
    """
    Convert check dictionaries into Markdown bullet points.
    """
    if not checks:
        return "- None\n"

    lines = []

    for check in checks:
        lines.append(f"- {check['name']}: {check['details']}")

    return "\n".join(lines) + "\n"


def _make_recommendation(summary):
    """
    Create a short recommendation based on the analysis result.
    """
    if summary["result"] == "PASS":
        return (
            "No immediate issue detected by the automated pre-analysis. "
            "The logfile can be used for further manual review if needed."
        )

    return (
        "Review the failed checks before using this logfile as validation "
        "evidence. The issue should be confirmed against the test setup and "
        "expected ECU behavior."
    )


def generate_markdown_report(
    input_file,
    archive_path,
    summary,
    reports_dir="reports",
):
    """
    Generate a Markdown report for one analyzed logfile.

    Args:
        input_file: Original logfile path.
        archive_path: Archived logfile path.
        summary: Result dictionary from run_preanalysis().
        reports_dir: Output directory for reports.

    Returns:
        Path: Path to the generated report.
    """
    input_path = Path(input_file)
    archive_path = Path(archive_path)

    output_dir = Path(reports_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report_filename = f"{input_path.stem}_report.md"
    report_path = output_dir / report_filename

    passed_checks = _format_check_list(summary["passed_checks"])
    failed_checks = _format_check_list(summary["failed_checks"])
    detected_states = ", ".join(summary["detected_states"])
    recommendation = _make_recommendation(summary)

    report_content = f"""# ECU Log Pre-Analysis Report

## Summary

| Field | Value |
|---|---|
| Input file | `{input_path}` |
| Archive path | `{archive_path}` |
| Rows analyzed | {summary["row_count"]} |
| Detected ECU states | {detected_states} |
| Result | **{summary["result"]}** |

## Passed Checks

{passed_checks}

## Failed Checks

{failed_checks}

## Recommendation

{recommendation}
"""

    report_path.write_text(report_content, encoding="utf-8")

    return report_path