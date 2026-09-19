from abc import ABC,abstractmethod

from app.rag.models import Chunk

class VectorStore(ABC):
    
    @abstractmethod
    def add(
        self,
        chunks:list[Chunk],
        vectors:list[list[float]],
    )->None:
        pass