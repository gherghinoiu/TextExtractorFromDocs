import pytest
import os
from locallib.ingest import ingest_file

# 1. Test TXT Files
def test_txt_ingestion(tmp_path):
    # tmp_path is a pytest trick: it creates a temporary folder that auto-deletes later
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("Hello World", encoding="utf-8")
    
    result = ingest_file(str(p))
    
    assert result.file_type == "txt"
    assert result.content == "Hello World"
    assert "created_date" in result.metadata

# 2. Test Error Handling (Non-existent file)
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        ingest_file("non_existent_file.txt")

# 3. Test Unsupported File
def test_unsupported_extension(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "image.png"
    p.write_text("fake image content")
    
    with pytest.raises(ValueError, match="Unsupported"):
        ingest_file(str(p))

# 4. Test PDF (Using a Mock/Fake function)
# We don't want to run Docker in unit tests (too slow). 
# We just check if the ROUTER calls the PDF parser.
from unittest.mock import patch

@patch('locallib.ingest.parse_pdf')
def test_pdf_routing(mock_parse, tmp_path):
    # Setup: Create a fake empty PDF file
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test.pdf"
    p.write_bytes(b"%PDF-1.5...") # minimal fake header
    
    # Run
    ingest_file(str(p))
    
    # Assert: Did we actually call the PDF parser?
    mock_parse.assert_called_once()