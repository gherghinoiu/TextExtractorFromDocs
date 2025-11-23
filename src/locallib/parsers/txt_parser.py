import os
import datetime
from ..schemas import FileContent

def get_basic_metadata(file_path: str) -> dict:
    """Helper to extract OS-level metadata common to all files."""
    stats = os.stat(file_path)
    return {
        "file_name": os.path.basename(file_path),
        "file_size_bytes": stats.st_size,
        # Convert timestamp to readable string
        "created_date": datetime.datetime.fromtimestamp(stats.st_ctime).isoformat(),
        "modified_date": datetime.datetime.fromtimestamp(stats.st_mtime).isoformat(),
    }

def parse_txt(file_path: str) -> FileContent:
    """
    Reads a standard .txt file.
    """
    # 1. Read Content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        # Fallback if utf-8 fails (common in Windows logs)
        with open(file_path, 'r', encoding='latin-1') as f:
            text = f.read()

    # 2. Get Metadata
    meta = get_basic_metadata(file_path)

    # 3. Return Standard Object
    return FileContent(
        file_type="txt",
        content=text,
        metadata=meta
    )