from pathlib import Path

from ecu_log_tool.report import generate_markdown_report


def test_generate_markdown_report_creates_file(tmp_path):
    input_file = Path("sample_logs/brc_valid_log.csv")
    archive_path = Path("archive/20260627_224047_brc_valid_log.csv")

    summary = {
        "result": "PASS",
        "row_count": 6,
        "detected_states": ["CRITICAL", "NORMAL", "WARN"],
        "passed_checks": [
            {
                "name": "Known ECU states",
                "passed": True,
                "details": "All ECU states are known.",
            }
        ],
        "failed_checks": [],
    }

    report_path = generate_markdown_report(
        input_file=input_file,
        archive_path=archive_path,
        summary=summary,
        reports_dir=tmp_path,
    )

    assert report_path.exists()
    assert report_path.name == "brc_valid_log_report.md"

    report_content = report_path.read_text(encoding="utf-8")

    assert "# ECU Log Pre-Analysis Report" in report_content
    assert "| Rows analyzed | 6 |" in report_content
    assert "| Result | **PASS** |" in report_content
    assert "Known ECU states" in report_content
    assert "- None" in report_content