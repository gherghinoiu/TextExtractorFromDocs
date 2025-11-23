#import sys
import os
from pypdf import PdfWriter

#sys.path.append(os.path.join(os.getcwd(), 'src'))
from locallib.ingest import ingest_file

# 1. Create a Dummy PDF
writer = PdfWriter()
writer.add_blank_page(width=200, height=200)
# Note: Adding text to a PDF via pypdf writer is complex. 
# For this test, we will accept that it finds specific metadata 
# or we create an empty PDF and see if it runs without crashing.
writer.add_metadata({"/Author": "PDF_User"})
with open("test.pdf", "wb") as f:
    writer.write(f)

# 2. Test Ingestion
try:
    print("--- Testing PDF Ingestion ---")
    #result = ingest_file("Adresa_inaintare_raportare_bianuala_PNRR_2063.pdf")
    result = ingest_file("testing.pdf")
    print(f"Type: {result.file_type}")
    # It will likely say [SCANNED...] because we didn't write text content, 
    # but it proves the parser is running!
    print(f"Content Preview: {result.content[:5000]}") 
    print(f"Author: {result.metadata.get('created_author')}")
    print("--- SUCCESS ---")
except Exception as e:
    print(f"--- FAILED: {e}")

# 3. Cleanup
if os.path.exists("test.pdf"):
    os.remove("test.pdf")


    