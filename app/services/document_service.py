from uuid import uuid4

from fastapi import UploadFile

from app.infrastructure.storage.local_storage import LocalStorage
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import (
    DocumentResponse,
    DocumentStatus,
)

class DocumentService:
    
    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".txt",
        ".md",
    }
    
    def __init__(
        self,
        repository:DocumentRepository,
        storage:LocalStorage,
    )->None:
        self.repository = repository
        self.storage = storage
    
    async def upload_document(
        self,
        file:UploadFile,
    )->DocumentResponse:
        
        filename = file.filename
        if not filename:
            raise ValueError("Filename is required!")

        extension = self._get_extension(filename)
        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type:{extension}"
            )
        
        document_id = str(uuid4())
        
        await self.storage.save(
            document_id=document_id,
            file=file
        )
        
        document = DocumentResponse(
            id=document_id,
            filename=filename,
            content_type=file.content_type,
            status=DocumentStatus.UPLOADED
        )
        return self.repository.save(document)
    
    def get_document(
        self,
        document_id:str,
    )->DocumentResponse|None:
        return self.repository.get(document_id)
    
    @staticmethod
    def _get_extension(filename:str)->str:
        index = filename.rfind(".")
        
        if index == -1:
            return ""
        
        return filename[index:].lower()