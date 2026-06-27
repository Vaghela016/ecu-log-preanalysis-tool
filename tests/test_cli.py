import os

from ecu_log_tool.cli import main


def test_cli_valid_log_returns_zero(capsys):
    exit_code = main(["analyze", "sample_logs/brc_valid_log.csv"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "ECU Log Pre-Analysis" in captured.out
    assert "Result: PASS" in captured.out
    assert "Rows analyzed: 6" in captured.out


def test_cli_critical_fault_log_returns_one(capsys):
    exit_code = main(["analyze", "sample_logs/brc_critical_fault.csv"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Result: FAIL" in captured.out
    assert "CRITICAL state error code" in captured.out
    assert "CRITICAL PWM shutdown" in captured.out


def test_cli_bad_timestamp_log_returns_one(capsys):
    exit_code = main(["analyze", "sample_logs/brc_bad_timestamp.csv"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Result: FAIL" in captured.out
    assert "Monotonic timestamps" in captured.out