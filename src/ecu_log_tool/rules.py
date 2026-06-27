"""
Rule-based pre-analysis for ECU logfiles.

The rules in this module simulate a first automatic check of embedded-system
test logs before deeper manual analysis.
"""

ALLOWED_STATES = {"NORMAL", "WARN", "CRITICAL"}


def _make_check(name, passed, details):
    """
    Create a simple check result dictionary.
    """
    return {
        "name": name,
        "passed": passed,
        "details": details,
    }


def check_unknown_states(rows):
    """
    Check whether all ECU states are known.
    """
    detected_states = {row["state"] for row in rows}
    unknown_states = sorted(detected_states - ALLOWED_STATES)

    if unknown_states:
        return _make_check(
            "Known ECU states",
            False,
            "Unknown state(s): " + ", ".join(unknown_states),
        )

    return _make_check(
        "Known ECU states",
        True,
        "All ECU states are known.",
    )


def check_critical_error_code(rows):
    """
    Check that every CRITICAL row has a non-zero error code.
    """
    failing_rows = []

    for index, row in enumerate(rows, start=1):
        if row["state"] == "CRITICAL" and row["error_code"] == 0:
            failing_rows.append(index)

    if failing_rows:
        return _make_check(
            "CRITICAL state error code",
            False,
            "CRITICAL row(s) with error_code 0: " + str(failing_rows),
        )

    return _make_check(
        "CRITICAL state error code",
        True,
        "All CRITICAL rows have non-zero error codes.",
    )


def check_critical_pwm_zero(rows):
    """
    Check that pwm_duty is 0 during CRITICAL state if pwm_duty is present.
    """
    failing_rows = []

    for index, row in enumerate(rows, start=1):
        if (
            row["state"] == "CRITICAL"
            and row["signal"] == "pwm_duty"
            and row["value"] != 0
        ):
            failing_rows.append(index)

    if failing_rows:
        return _make_check(
            "CRITICAL PWM shutdown",
            False,
            "CRITICAL pwm_duty row(s) not equal to 0: " + str(failing_rows),
        )

    return _make_check(
        "CRITICAL PWM shutdown",
        True,
        "No CRITICAL pwm_duty violation detected.",
    )


def check_monotonic_timestamps(rows):
    """
    Check that timestamps are monotonically increasing.

    Equal timestamps are allowed. A later timestamp must not be smaller than
    the previous timestamp.
    """
    failing_rows = []

    previous_timestamp = rows[0]["timestamp_ms"]

    for index, row in enumerate(rows[1:], start=2):
        current_timestamp = row["timestamp_ms"]

        if current_timestamp < previous_timestamp:
            failing_rows.append(index)

        previous_timestamp = current_timestamp

    if failing_rows:
        return _make_check(
            "Monotonic timestamps",
            False,
            "Timestamp decrease detected at row(s): " + str(failing_rows),
        )

    return _make_check(
        "Monotonic timestamps",
        True,
        "Timestamps are monotonically increasing.",
    )


def run_preanalysis(rows):
    """
    Run all pre-analysis checks.

    Args:
        rows: Parsed logfile rows.

    Returns:
        dict: Summary containing result, passed checks, and failed checks.
    """
    checks = [
        check_unknown_states(rows),
        check_critical_error_code(rows),
        check_critical_pwm_zero(rows),
        check_monotonic_timestamps(rows),
    ]

    passed_checks = [check for check in checks if check["passed"]]
    failed_checks = [check for check in checks if not check["passed"]]

    result = "PASS"

    if failed_checks:
        result = "FAIL"

    detected_states = sorted({row["state"] for row in rows})

    return {
        "result": result,
        "row_count": len(rows),
        "detected_states": detected_states,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
    }