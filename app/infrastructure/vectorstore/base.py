from abc import ABC,abstractmethod

from app.rag.models import(
    Chunk,
    RetrievalResult,
)

class VectorStore(ABC):
    
    @abstractmethod
    def add(
        self,
        chunks:list[Chunk],
        vectors:list[list[float]],
    )->None:
        pass
    
    @abstractmethod
    def search(
        self,
        query_vector:list[float],
        top_k:int=5,
    )->list[RetrievalResult]:
        pass