import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    """Extracts and cleans text from a PDF file."""
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File '{pdf_path}' not found.")
        return ""

    with pdfplumber.open(pdf_path) as pdf:
        # 🔥 Fix formatting issues by replacing newlines with spaces
        text = " ".join([page.extract_text().replace("\n", " ") for page in pdf.pages if page.extract_text()])

    print("\n✅ Extracted Resume Text (First 500 characters):\n")
    print(text[:500])  # Debugging print

    return text