from app.infrastructure.vectorstore.base import(
    VectorStore,
)
from app.rag.embeddings.base import(
    EmbeddingProvider,
)
from app.rag.models import RetrievalResult

class RetrievalService:
    
    def __init__(
        self,
        embedding_provider:EmbeddingProvider,
        vector_store:VectorStore,
    )->None:
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store
        
    def retrieve(
        self,
        query:str,
        top_k:int = 5,
    )->list[RetrievalResult]:
        
        if not query.strip():
            raise ValueError(
                "Query can't be empty!"
            )
        
        query_vector = (
            self.embedding_provider.embed_text(
                query
            )
        )
        
        results = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
        )
        
        return results