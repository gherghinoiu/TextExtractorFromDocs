# Local Library (File Ingestion Tool)

A standardized Python library for extracting text and metadata from various file formats. It is designed to run on restricted environments by offloading OCR tasks to a Docker container.

## Features
* **Input:** Accepts file paths (`.txt`, `.docx`, `.xlsx`, `.pdf`).
* **Output:** Returns a standardized `FileContent` object (content, metadata, file_type).
* **OCR:** Automatically detects scanned PDFs and uses a Docker container (`local-ocr`) to extract text.
* **Romanian Support:** OCR is optimized for Romanian language and handles mixed English/Romanian documents.
* **Auto-Rotation:** Automatically fixes sideways or upside-down scanned pages.
* **Table Optimization:** Includes deskewing and cleaning algorithms to improve table extraction.

## Prerequisites
* Python 3.9+
* Docker Desktop (Running)

## Installation

### 1. Developer Setup (Local)
To modify the library or run it on your machine:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd local_library
    ```

2.  **Install in editable mode:**
    ```bash
    pip install -e .[dev]
    ```

3.  **Build the Docker OCR Image (Crucial):**
    This builds the custom image with Romanian language support.
    ```bash
    docker build -t local-ocr .
    ```

### 2. Usage in Another Project
To use this library in a different project/folder:

```bash
pip install git+[https://github.com/YourUsername/local_library.git](https://github.com/YourUsername/local_library.git)
```
*(Note: The machine must still have Docker Desktop running and the `local-ocr` image built).*

## Usage Example

```python
from locallib.ingest import ingest_file

file_path = "C:/Users/gherg/Documents/scanned_invoice.pdf"

try:
    # Ingests docx, xlsx, txt, or pdf
    result = ingest_file(file_path)
    
    print(f"Type: {result.file_type}")
    print(f"Author: {result.metadata.get('created_author')}")
    print(f"Content Preview: {result.content[:200]}...")

except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"Error: {e}")
```

## OCR Strategy & Architecture

The PDF parser uses a **"Safe & Smart"** approach to balance speed and accuracy:

1.  **Native Text Check (Fast):** * The system first attempts to read text directly using Python (`pypdf`). 
    * If readable text is found, it returns immediately (taking <1 second).
    
2.  **Scanned Detection (Fallback):**
    * If the file has pages but almost zero text (<50 chars), it flags the file as "Scanned".
    * It triggers the `local-ocr` Docker container.

3.  **Docker Configuration:**
    The container runs `ocrmypdf` with specific flags for this use case:
    * `--force-ocr`: Ignores existing artifacts to allow proper page rotation.
    * `--rotate-pages`: Uses OSD (Orientation Script Detection) to fix sideways/upside-down pages.
    * `--deskew` & `--clean`: Straightens images and removes noise to help with **Table Extraction**.
    * `-l ron+eng`: Uses both Romanian and English dictionaries simultaneously.

## Testing

Run the automated test suite (requires `pytest`):

```bash
pytest
```