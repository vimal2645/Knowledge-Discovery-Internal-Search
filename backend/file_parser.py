import PyPDF2
from docx import Document
import os

def extract_text_from_file(filepath):
    """Extract text content from various file formats"""
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    
    try:
        if ext == '.txt':
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        elif ext == '.pdf':
            text = []
            with open(filepath, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        
        elif ext in ['.docx', '.doc']:
            doc = Document(filepath)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        
        else:
            return ""
    
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return ""

def get_file_category(filename):
    """Auto-categorize files based on filename patterns"""
    filename_lower = filename.lower()
    
    # Check for keywords in filename
    if any(word in filename_lower for word in ['report', 'analysis', 'summary', 'data']):
        return 'Reports'
    
    if any(word in filename_lower for word in ['campaign', 'ad', 'marketing', 'promotion']):
        return 'Campaigns'
    
    if any(word in filename_lower for word in ['presentation', 'slide', 'ppt', 'deck']):
        return 'Presentations'
    
    if any(word in filename_lower for word in ['guide', 'manual', 'doc', 'documentation', 'readme', 'guidelines']):
        return 'Documentation'
    
    # Default category
    return 'General'
