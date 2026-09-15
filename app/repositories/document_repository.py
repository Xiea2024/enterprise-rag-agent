from abc import ABC,abstractmethod

from app.schemas.document import DocumentResponse

class DocumentRepository(ABC):
    
    @abstractmethod
    def save(
        self,
        document:DocumentResponse,
    )->DocumentResponse:
        pass
    
    
    @abstractmethod
    def get(
        self,
        document_id:str,
        )->DocumentResponse|None:
        pass
    
class InMemoryDocumentRepository(DocumentRepository):
    
    def __init__(self)->None:
        self._documents:dict[str,DocumentResponse] = {}
        
    def save(self, document: DocumentResponse) -> DocumentResponse:
        self._documents[document.id] = document
        return document
    
    def get(self, document_id: str) -> DocumentResponse | None:
        return self._documents.get(document_id)