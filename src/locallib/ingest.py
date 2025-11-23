import pathlib
import os
from .schemas import FileContent
from .parsers.txt_parser import parse_txt
from .parsers.office_parser import parse_docx, parse_xlsx
# --- NEW IMPORT ---
from .parsers.pdf_parser import parse_pdf

def ingest_file(file_path: str) -> FileContent:
    # ... (Same setup code) ...
    
    path = pathlib.Path(file_path) # Re-adding context for safety
    extension = path.suffix.lower()
    
    if not path.exists(): raise FileNotFoundError(f"File not found: {file_path}")
    if not path.is_file(): raise ValueError(f"Path is not a file: {file_path}")

    if extension == ".txt":
        return parse_txt(file_path)
        
    elif extension in [".docx", ".doc"]:
        if extension == ".doc": raise ValueError("Legacy .doc format not supported")
        return parse_docx(file_path)
        
    elif extension in [".xlsx", ".xls"]:
        if extension == ".xls": raise ValueError("Legacy .xls format not supported")
        return parse_xlsx(file_path)
    
    elif extension == ".csv":
        return parse_txt(file_path)
        
    # --- UPDATED LOGIC ---
    elif extension == ".pdf":
        return parse_pdf(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")