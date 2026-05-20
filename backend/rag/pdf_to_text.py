import pdfplumber

def pdf_to_text(pdf_path : str ) -> list:
    with pdfplumber.open(pdf_path) as pdf:
        pages = []
        for i, page in enumerate(pdf.pages):
            pages.append({"text": page.extract_text() or "", "page": i + 1})

    for page in pages:
        page["text"] = "\n".join([line.strip() for line in page["text"].split("\n") if line.split()])
    return pages
