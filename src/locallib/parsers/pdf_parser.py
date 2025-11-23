import os
import subprocess
import pathlib
from pypdf import PdfReader
from ..schemas import FileContent
from .txt_parser import get_basic_metadata

def run_ocr_docker(file_path: str) -> str:
    """
    Runs a Docker container to perform OCR on the file.
    Returns the extracted text.
    Uses 'Safe' settings: respects existing text, standard rotation thresholds.
    """
    # 1. Prepare Paths (Windows Safe)
    path = pathlib.Path(file_path).resolve()
    directory = str(path.parent).replace('\\', '/')
    filename = path.name
    output_txt = f"{filename}.txt"
    output_pdf = f"{filename}_ocr.pdf"

    # print(f"DEBUG: Docker Mount Directory: '{directory}'") # Uncomment if debugging is needed

    # 2. Construct Command
    cmd = [
        "docker", "run", "--rm",
        "-w", "/home/docker",
        "-v", f"{directory}:/home/docker",
        "local-ocr", 
        
        # --- SAFE CONFIGURATION ---
        "--skip-text",      # If text exists, keep it. Don't force re-OCR.
        "--rotate-pages",   # Fix orientation if standard confidence is high.
        "--deskew",         # Straighten crooked scans.
        "--clean",          # Remove visual noise/dots.
        
        "-l", "ron+eng",    # Romanian + English
        "--sidecar", output_txt,
        filename,       
        output_pdf      
    ]

    try:
        # Run silently (capture_output=True)
        subprocess.run(cmd, check=True, capture_output=True)
        
        # 3. Read Result
        txt_path = path.parent / output_txt
        if txt_path.exists():
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 4. Cleanup Temporary Files
            os.remove(txt_path)
            
            # Optional: We remove the OCR'd PDF to keep the user's folder clean.
            # If you want to keep the "fixed" PDF, comment out the next two lines.
            pdf_out = path.parent / output_pdf
            if pdf_out.exists():
                os.remove(pdf_out)
                
            return content
        else:
            return "[ERROR: OCR finished but no text file was created]"

    except subprocess.CalledProcessError as e:
        # Only print if something actually crashes the process
        err_msg = e.stderr.decode('utf-8') if e.stderr else "Unknown Docker Error"
        print(f"OCR FAILED. Error output:\n{err_msg}")
        return "[ERROR: OCR Failed via Docker]"
    except Exception as e:
        return f"[ERROR: {str(e)}]"


def parse_pdf(file_path: str) -> FileContent:
    """
    Extracts text from a PDF. 
    Handles both Native and Scanned (via OCR).
    """
    reader = PdfReader(file_path)
    
    # 1. Attempt Native Text Extraction (The Fast Way)
    full_text = []
    try:
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
    except Exception as e:
        print(f"WARNING: Native extraction failed slightly: {e}")
    
    content = "\n".join(full_text)

    # 2. Check for Scanned PDF
    # Logic: If we have pages but < 50 chars of text, assume it's an image.
    if len(reader.pages) > 0 and len(content.strip()) < 50:
        print(f"DEBUG: File '{pathlib.Path(file_path).name}' appears scanned. Running OCR...")
        content = run_ocr_docker(file_path)

    # 3. Extract Metadata
    meta = get_basic_metadata(file_path)
    if reader.metadata:
        if reader.metadata.author:
            meta["created_author"] = reader.metadata.author
        if reader.metadata.creation_date:
            meta["created_date_internal"] = str(reader.metadata.creation_date)

    return FileContent(file_type="pdf", content=content, metadata=meta)