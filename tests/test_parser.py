from pathlib import Path

from ecu_log_tool.parser import read_csv_log, validate_required_columns


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_read_valid_brc_log():
    log_path = PROJECT_ROOT / "sample_logs" / "brc_valid_log.csv"

    rows = read_csv_log(log_path)

    assert len(rows) == 6
    assert rows[0]["ecu"] == "BRC"
    assert rows[0]["state"] == "NORMAL"
    assert rows[0]["timestamp_ms"] == 0
    assert rows[0]["value"] == 300
    assert rows[0]["error_code"] == 0


def test_validate_required_columns_detects_missing_column():
    fieldnames = [
        "timestamp_ms",
        "ecu",
        "state",
        "signal",
        "value",
    ]

    missing_columns = validate_required_columns(fieldnames)

    assert missing_columns == ["error_code"]