import docx
import fitz  # PyMuPDF
import os

def extract_text_from_docx(file_path):
    """
    Extracts text from a .docx file.
    """
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\\n'.join(full_text)
    except Exception as e:
        return f"An error occurred while processing {file_path}: {e}"

def extract_text_from_pdf(file_path):
    """
    Extracts text from a .pdf file.
    """
    try:
        doc = fitz.open(file_path)
        full_text = []
        for page in doc:
            full_text.append(page.get_text())
        return '\\n'.join(full_text)
    except Exception as e:
        return f"An error occurred while processing {file_path}: {e}"

def extract_text(file_path):
    """
    Extracts text from a file based on its extension.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
        
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    else:
        return f"Unsupported file type: {file_extension}"

def extract_all_pdfs_in_directory(directory, output_file):
    """
    Extracts text from all PDF files in a directory and its subdirectories,
    and saves the combined text to an output file.
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    file_path = os.path.join(root, file)
                    outfile.write(f"--- START OF FILE: {file_path} ---\\n\\n")
                    text = extract_text_from_pdf(file_path)
                    outfile.write(text)
                    outfile.write(f"\\n\\n--- END OF FILE: {file_path} ---\\n\\n")

if __name__ == '__main__':
    # Example usage:
    file_to_extract = "Course/References/SBM_IRB.docx"
    print(extract_text(file_to_extract))
    references_directory = "Course/References"
    output_text_file = "references_text.txt"
    extract_all_pdfs_in_directory(references_directory, output_text_file)
    print(f"Text from all PDF files has been extracted and saved to {output_text_file}")
