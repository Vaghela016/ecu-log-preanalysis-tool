from ecu_log_tool.rules import run_preanalysis


def test_valid_log_passes_all_rules():
    rows = [
        {
            "timestamp_ms": 0,
            "ecu": "BRC",
            "state": "NORMAL",
            "signal": "ntc_raw",
            "value": 300,
            "error_code": 0,
        },
        {
            "timestamp_ms": 10,
            "ecu": "BRC",
            "state": "CRITICAL",
            "signal": "pwm_duty",
            "value": 0,
            "error_code": 2,
        },
    ]

    summary = run_preanalysis(rows)

    assert summary["result"] == "PASS"
    assert len(summary["passed_checks"]) == 4
    assert len(summary["failed_checks"]) == 0


def test_unknown_state_fails():
    rows = [
        {
            "timestamp_ms": 0,
            "ecu": "BRC",
            "state": "BOOTING",
            "signal": "ntc_raw",
            "value": 300,
            "error_code": 0,
        }
    ]

    summary = run_preanalysis(rows)

    assert summary["result"] == "FAIL"
    assert any(
        check["name"] == "Known ECU states"
        for check in summary["failed_checks"]
    )


def test_critical_state_with_zero_error_code_fails():
    rows = [
        {
            "timestamp_ms": 0,
            "ecu": "BRC",
            "state": "CRITICAL",
            "signal": "ntc_raw",
            "value": 980,
            "error_code": 0,
        }
    ]

    summary = run_preanalysis(rows)

    assert summary["result"] == "FAIL"
    assert any(
        check["name"] == "CRITICAL state error code"
        for check in summary["failed_checks"]
    )


def test_critical_pwm_not_zero_fails():
    rows = [
        {
            "timestamp_ms": 0,
            "ecu": "BRC",
            "state": "CRITICAL",
            "signal": "pwm_duty",
            "value": 50,
            "error_code": 2,
        }
    ]

    summary = run_preanalysis(rows)

    assert summary["result"] == "FAIL"
    assert any(
        check["name"] == "CRITICAL PWM shutdown"
        for check in summary["failed_checks"]
    )


def test_decreasing_timestamp_fails():
    rows = [
        {
            "timestamp_ms": 20,
            "ecu": "BRC",
            "state": "NORMAL",
            "signal": "ntc_raw",
            "value": 300,
            "error_code": 0,
        },
        {
            "timestamp_ms": 10,
            "ecu": "BRC",
            "state": "NORMAL",
            "signal": "pwm_duty",
            "value": 100,
            "error_code": 0,
        },
    ]

    summary = run_preanalysis(rows)

    assert summary["result"] == "FAIL"
    assert any(
        check["name"] == "Monotonic timestamps"
        for check in summary["failed_checks"]
    )