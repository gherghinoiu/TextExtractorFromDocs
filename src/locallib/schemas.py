from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class FileContent:
    """
    Standardized output for any processed file.
    """
    file_type: str                # e.g., 'pdf', 'docx', 'txt'
    content: str                  # The raw extracted text
    metadata: Dict[str, Any] = field(default_factory=dict) # e.g., {'author': 'John', 'date': '2023...'}