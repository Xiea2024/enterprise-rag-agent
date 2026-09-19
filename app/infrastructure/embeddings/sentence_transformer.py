from sentence_transformers import SentenceTransformer

from app.rag.embeddings.base import EmbeddingProvider


class SentenceTransformerEmbedding(
    EmbeddingProvider
):
    
    def __init__(
        self,
        model_name:str,
    )->None:
        self.model = SentenceTransformer(model_name)
        
        self._dimension = (
            self.model.get_embedding_dimension()
        )
        
        if self._dimension is None:
            raise ValueError(
                "Unable to determine embedding dimension"
            )
    
    @property
    def dimension(self) -> int:
        return self._dimension # type: ignore
    
    def embed_text(
        self,
        text:str,
    )->list[float]:
        
        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )
        
        return vector.tolist()
    
    def embed_documents(
        self, texts: list[str]
        ) -> list[list[float]]:
        
        if not texts:
            return []
        
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
        )
        
        return vectors.tolist()
    
    