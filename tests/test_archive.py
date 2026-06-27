from pathlib import Path

from ecu_log_tool.archive import archive_logfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_archive_logfile_creates_copy(tmp_path):
    source_log = PROJECT_ROOT / "sample_logs" / "brc_valid_log.csv"
    archive_dir = tmp_path / "archive"

    archived_path = archive_logfile(source_log, archive_dir)

    assert archived_path.exists()
    assert archived_path.is_file()
    assert archived_path.name.endswith("brc_valid_log.csv")
    assert archived_path.read_text(encoding="utf-8") == source_log.read_text(
        encoding="utf-8"
    )