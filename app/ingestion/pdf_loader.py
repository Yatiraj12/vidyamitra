from pdf2image import convert_from_path
import pytesseract

# Explicit Windows paths
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\Users\91807\Downloads\Release-25.12.0-0\Library\bin"

# def load_pdf_text(pdf_path):
#     pages = convert_from_path(
#         pdf_path,
#         poppler_path=POPPLER_PATH
    # )
# def load_pdf_text(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return f.read()

def load_pdf_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

    all_text = []

    for page in pages:
        text = pytesseract.image_to_string(page, lang="eng")
        if text.strip():
            all_text.append(text)

    return "\n".join(all_text)
