from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile
)

from app.infrastructure.storage.local_storage import LocalStorage
from app.repositories.document_repository import(
    InMemoryDocumentRepository
)
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

repository = InMemoryDocumentRepository()
storage = LocalStorage()

document_service = DocumentService(
    repository=repository,
    storage=storage,
)

@router.post(
    "",response_model=DocumentResponse,
    status_code=201
)
async def upload_document(
    file:UploadFile=File(...),
)->DocumentResponse:
    
    try:
        return await document_service.upload_document(file=file)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)        
def get_document(
    document_id:str,
    )->DocumentResponse:
    document = document_service.get_document(document_id)
    
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found!",
        )
        
    return document
    
