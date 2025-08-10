import os
import hashlib
import aiofiles
from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_uploaded_file(self, file: UploadFile) -> tuple[str, str]:
        """Save uploaded file and return filename and hash"""
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}-{file.filename}"
        file_path = os.path.join(self.upload_dir, filename)
        
        # Read file content
        content = await file.read()
        
        # Calculate file hash
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        return filename, file_hash

    def extract_text_from_file(self, filename: str) -> str:
        """Extract text content from PDF or DOCX file"""
        file_path = os.path.join(self.upload_dir, filename)
        
        try:
            if filename.lower().endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif filename.lower().endswith('.docx'):
                loader = Docx2txtLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {filename}")
            
            documents = loader.load_and_split()
            content = ""
            for page in documents:
                content += page.page_content
            
            return content
            
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {str(e)}")
            return ""

    def is_allowed_file(self, filename: str) -> bool:
        """Check if file type is allowed"""
        return filename.lower().endswith(('.pdf', '.docx'))

    async def delete_file(self, filename: str) -> bool:
        """Delete uploaded file"""
        try:
            file_path = os.path.join(self.upload_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {filename}: {str(e)}")
            return False


# Global document service instance
document_service = DocumentService()