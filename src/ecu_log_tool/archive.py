"""
Logfile archiving module for the ECU Log Pre-Analysis Tool.

This module copies the original logfile into an archive folder using
a timestamped filename. The original file is not modified.
"""

from pathlib import Path
from datetime import datetime
import shutil


class ArchiveError(Exception):
    """Raised when a logfile cannot be archived."""


def archive_logfile(file_path, archive_dir="archive"):
    """
    Archive a logfile by copying it into the archive folder.

    Args:
        file_path: Path to the original logfile.
        archive_dir: Target archive directory.

    Returns:
        Path: Path to the archived copy.

    Raises:
        ArchiveError: If the input path is invalid.
    """
    source_path = Path(file_path)

    if not source_path.exists():
        raise ArchiveError(f"Logfile not found: {source_path}")

    if not source_path.is_file():
        raise ArchiveError(f"Path is not a file: {source_path}")

    target_dir = Path(archive_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_filename = f"{timestamp}_{source_path.name}"
    archive_path = target_dir / archive_filename

    shutil.copy2(source_path, archive_path)

    return archive_path