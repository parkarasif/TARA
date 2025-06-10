import docx
import pdfminer.high_level

def parse_resume(file_path):
    if file_path.endswith('.pdf'):
        return pdfminer.high_level.extract_text(file_path)
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs])
    elif file_path.endswith('.txt'):
        return open(file_path, encoding='utf-8').read()
    else:
        raise ValueError("Unsupported file type")