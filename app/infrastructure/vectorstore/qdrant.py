from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.infrastructure.vectorstore.base import(
    VectorStore,
)

from app.rag.models import Chunk

class QdrantVectorStore(VectorStore):
    
    def __init__(
        self,
        url:str,
        collection_name:str,
        vector_size:int,
    )->None:
        
        self.client = QdrantClient(
            url=url,
        )
        
        self.collection_name = collection_name
        self.vector_size = vector_size
        
        self._ensure_collection()
        
    def _ensure_collection(self)->None:
        
        if self.client.collection_exists(
            self.collection_name
        ):
            return
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )
        
    
    def add(
        self,
        chunks:list[Chunk],
        vectors:list[list[float]]
    )->None:
        
        if len(chunks) != len(vectors):
            raise ValueError(
                "Chunks and vectors must"
                "have the same length"
            )
        
        points = []
        
        for chunk,vector in zip(
            chunks,
            vectors,
        ):
            points.append(
                PointStruct(
                    id = chunk.id,
                    vector=vector,
                    payload={
                      "document_id":chunk.document_id,
                      "chunk_index":chunk.chunk_index,
                      "text":chunk.text,
                      "page_number":chunk.page_number,
                      "metadata":chunk.metadata,                    
                    },
                )
            )
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )