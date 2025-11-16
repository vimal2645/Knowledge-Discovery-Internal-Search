import os

class Config:
    """Application configuration"""
    UPLOAD_FOLDER = 'uploads'
    INDEX_DIR = 'indexdir'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}
    
    # Create directories if they don't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(INDEX_DIR, exist_ok=True)
