import fitz  # PyMuPDF
import sys
import json

def search_text_in_pdf(file_path, search_text):
    try:
        pdf_document = fitz.open(file_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text = page.get_text("text")
            if search_text.lower() in text.lower():
                pdf_document.close()
                return True
        pdf_document.close()
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
    return False

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Usage: python search_pdf_content.py <pdf_file_path> <search_text>", file=sys.stderr)
        sys.exit(1)
    
    pdf_file_path = sys.argv[1]
    search_text = sys.argv[2]
    result = search_text_in_pdf(pdf_file_path, search_text)
    print(json.dumps(result)) 