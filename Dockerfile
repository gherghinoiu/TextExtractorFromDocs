FROM jbarlow83/ocrmypdf

# Install Romanian language (ron) AND Orientation/Script Detection (osd)
RUN apt-get update && \
    apt-get install -y tesseract-ocr-ron tesseract-ocr-osd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*