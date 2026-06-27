"""
CSV logfile parser for the ECU Log Pre-Analysis Tool.

This module reads ECU test logs and prepares them for later rule-based
pre-analysis.
"""

from pathlib import Path
import csv


REQUIRED_COLUMNS = [
    "timestamp_ms",
    "ecu",
    "state",
    "signal",
    "value",
    "error_code",
]


NUMERIC_COLUMNS = [
    "timestamp_ms",
    "value",
    "error_code",
]


class LogParserError(Exception):
    """Raised when a logfile cannot be parsed correctly."""


def validate_required_columns(fieldnames):
    """
    Check whether all required CSV columns are present.
    """
    if fieldnames is None:
        return REQUIRED_COLUMNS.copy()

    missing_columns = []

    for column in REQUIRED_COLUMNS:
        if column not in fieldnames:
            missing_columns.append(column)

    return missing_columns


def _convert_numeric_fields(row, row_number):
    """
    Convert numeric CSV values from strings to integers.
    """
    converted_row = row.copy()

    for column in NUMERIC_COLUMNS:
        try:
            converted_row[column] = int(converted_row[column])
        except ValueError as error:
            raise LogParserError(
                f"Invalid numeric value in row {row_number}, "
                f"column '{column}': {converted_row[column]}"
            ) from error

    return converted_row


def read_csv_log(file_path):
    """
    Read and validate a CSV logfile.
    """
    path = Path(file_path)

    if not path.exists():
        raise LogParserError(f"Logfile not found: {path}")

    if not path.is_file():
        raise LogParserError(f"Path is not a file: {path}")

    rows = []

    with path.open(mode="r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        missing_columns = validate_required_columns(reader.fieldnames)

        if missing_columns:
            raise LogParserError(
                "Missing required column(s): " + ", ".join(missing_columns)
            )

        for row_number, row in enumerate(reader, start=2):
            cleaned_row = {}

            for key, value in row.items():
                if isinstance(value, str):
                    cleaned_row[key] = value.strip()
                else:
                    cleaned_row[key] = value

            converted_row = _convert_numeric_fields(cleaned_row, row_number)
            rows.append(converted_row)

    if not rows:
        raise LogParserError(f"Logfile is empty: {path}")

    return rows