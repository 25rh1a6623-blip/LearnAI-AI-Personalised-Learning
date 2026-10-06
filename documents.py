from pypdf import PdfReader
from docx import Document
def extract_text(f):
    if f.name.lower().endswith(".pdf"):
        return "\n".join((p.extract_text() or "") for p in PdfReader(f).pages)
    return "\n".join(p.text for p in Document(f).paragraphs)
