# ECU Log Pre-Analysis Tool

Small Python-based ECU logfile pre-analysis tool for embedded-system validation workflows.

This project was created as a focused portfolio project for a **System Verification / ECU Software Validation** working-student role. It simulates a realistic workflow where test logfiles are read, archived, checked against simple validation rules, and summarized in a Markdown report.

## Project Goal

The goal of this tool is to demonstrate a small but complete validation workflow:

1. Read ECU test logs from CSV files.
2. Validate required logfile columns.
3. Archive the original logfile with a timestamp.
4. Run rule-based pre-analysis checks.
5. Generate a PASS/FAIL summary.
6. Create a structured Markdown report.
7. Run the workflow locally on Windows and reproducibly in Docker.

## Relevance for System Verification

This project is relevant for automotive system verification because it demonstrates:

* logfile handling and pre-analysis
* manual and semi-automated test evaluation
* PASS/FAIL decision logic
* ECU-related signal checks
* structured documentation of validation results
* Python-based tooling for embedded test data
* pytest-based regression tests
* Docker-based reproducible execution

The sample logs are based on a simplified **Brake Resistor Control Unit / BRC** scenario.

## Example Log Format

```csv
timestamp_ms,ecu,state,signal,value,error_code
0,BRC,NORMAL,ntc_raw,300,0
10,BRC,NORMAL,pwm_duty,100,0
20,BRC,WARN,ntc_raw,760,1
30,BRC,WARN,pwm_duty,50,1
40,BRC,CRITICAL,ntc_raw,980,2
50,BRC,CRITICAL,pwm_duty,0,2
```

## Implemented Checks

The tool currently checks:

* required CSV columns must exist
* logfile must not be empty
* ECU states must be known
* `CRITICAL` state must have `error_code != 0`
* `CRITICAL` state must have `pwm_duty = 0` if PWM is present
* timestamps must be monotonically increasing

Allowed ECU states:

```text
NORMAL
WARN
CRITICAL
```

## Project Structure

```text
ecu-log-preanalysis-tool/
├── README.md
├── requirements.txt
├── Dockerfile
├── sample_logs/
│   ├── brc_valid_log.csv
│   ├── brc_critical_fault.csv
│   └── brc_bad_timestamp.csv
├── src/
│   └── ecu_log_tool/
│       ├── __init__.py
│       ├── parser.py
│       ├── archive.py
│       ├── rules.py
│       ├── report.py
│       └── cli.py
├── tests/
│   ├── test_parser.py
│   ├── test_archive.py
│   ├── test_rules.py
│   ├── test_report.py
│   └── test_cli.py
├── reports/
└── archive/
```

## Setup on Windows PowerShell

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

Set the Python path:

```powershell
$env:PYTHONPATH = "src"
```

Run the valid sample log:

```powershell
py -m ecu_log_tool.cli analyze sample_logs/brc_valid_log.csv
```

Expected result:

```text
ECU Log Pre-Analysis
Input file: sample_logs/brc_valid_log.csv
Archive path: archive\YYYYMMDD_HHMMSS_brc_valid_log.csv
Rows analyzed: 6
Result: PASS
Report generated: reports\brc_valid_log_report.md
```

Run a faulty sample log:

```powershell
py -m ecu_log_tool.cli analyze sample_logs/brc_critical_fault.csv
```

Expected result:

```text
Result: FAIL
Failed checks:
- CRITICAL state error code
- CRITICAL PWM shutdown
```

Run the bad timestamp sample log:

```powershell
py -m ecu_log_tool.cli analyze sample_logs/brc_bad_timestamp.csv
```

Expected result:

```text
Result: FAIL
Failed checks:
- Monotonic timestamps
```

## Run Automated Tests

```powershell
$env:PYTHONPATH = "src"
py -m pytest
```

Current expected result:

```text
12 passed
```

## Docker Usage

Build the Docker image:

```powershell
docker build -t ecu-log-preanalysis-tool .
```

Run the default valid-log analysis:

```powershell
docker run --rm ecu-log-preanalysis-tool
```

Run a specific logfile in Docker:

```powershell
docker run --rm ecu-log-preanalysis-tool python -m ecu_log_tool.cli analyze sample_logs/brc_critical_fault.csv
```

Inside Docker, paths are shown in Linux style, for example:

```text
archive/YYYYMMDD_HHMMSS_brc_valid_log.csv
reports/brc_valid_log_report.md
```

## Example Results

| Logfile                  | Expected Result | Purpose                                  |
| ------------------------ | --------------- | ---------------------------------------- |
| `brc_valid_log.csv`      | PASS            | valid reference log                      |
| `brc_critical_fault.csv` | FAIL            | detects unsafe critical-state behavior   |
| `brc_bad_timestamp.csv`  | FAIL            | detects non-monotonic timestamp sequence |

## Generated Reports

The tool generates Markdown reports in:

```text
reports/
```

Each report includes:

* input filename
* archive path
* number of rows
* detected ECU states
* passed checks
* failed checks
* short recommendation

Generated reports and archived logs are ignored by Git because they are runtime outputs.

## Limitations

This is a student-level validation portfolio project. It is intentionally small and does not claim to replace professional automotive validation tools.

Current limitations:

* CSV input only
* simplified ECU state model
* simplified BRC-inspired signals
* no CAN/LIN log decoding
* no real ECU connection
* no database backend
* no graphical user interface

Possible future extensions:

* FastAPI endpoint for analysis requests
* support for uploaded logfiles
* JSON output mode
* additional Seat Control Unit sample logs
* simple dashboard or GUI
* GitHub Actions workflow for automated pytest execution

## Skills Demonstrated

* Python logfile parsing
* rule-based pre-analysis
* Markdown report generation
* logfile archiving
* pytest regression testing
* Docker execution
* Windows PowerShell workflow
* Linux-style container execution
* Git-ready project structure
* embedded-system validation mindset
