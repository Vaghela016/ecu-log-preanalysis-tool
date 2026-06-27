"""
Command-line interface for the ECU Log Pre-Analysis Tool.

Example:
    py -m ecu_log_tool.cli analyze sample_logs/brc_valid_log.csv
"""

import argparse
import sys

from ecu_log_tool.parser import read_csv_log, LogParserError
from ecu_log_tool.archive import archive_logfile, ArchiveError
from ecu_log_tool.rules import run_preanalysis
from ecu_log_tool.report import generate_markdown_report


def analyze_logfile(logfile_path):
    """
    Run the complete ECU logfile pre-analysis workflow.

    Args:
        logfile_path: Path to the CSV logfile.

    Returns:
        int: Process exit code. 0 means success, 1 means failure.
    """
    try:
        rows = read_csv_log(logfile_path)
        archive_path = archive_logfile(logfile_path)
        summary = run_preanalysis(rows)
        report_path = generate_markdown_report(
            input_file=logfile_path,
            archive_path=archive_path,
            summary=summary,
        )

    except (LogParserError, ArchiveError) as error:
        print("ECU Log Pre-Analysis")
        print(f"Input file: {logfile_path}")
        print(f"Result: FAIL")
        print(f"Error: {error}")
        return 1

    print("ECU Log Pre-Analysis")
    print(f"Input file: {logfile_path}")
    print(f"Archive path: {archive_path}")
    print(f"Rows analyzed: {summary['row_count']}")
    print(f"Result: {summary['result']}")
    print(f"Report generated: {report_path}")

    if summary["failed_checks"]:
        print()
        print("Failed checks:")

        for check in summary["failed_checks"]:
            print(f"- {check['name']}: {check['details']}")

        return 1

    return 0


def build_argument_parser():
    """
    Create the command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        description="ECU logfile pre-analysis tool"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze one ECU CSV logfile",
    )

    analyze_parser.add_argument(
        "logfile",
        help="Path to the ECU CSV logfile",
    )

    return parser


def main(argv=None):
    """
    CLI entry point.
    """
    argument_parser = build_argument_parser()
    args = argument_parser.parse_args(argv)

    if args.command == "analyze":
        return analyze_logfile(args.logfile)

    return 1


if __name__ == "__main__":
    sys.exit(main())