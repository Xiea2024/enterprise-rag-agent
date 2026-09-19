from pathlib import Path
from app.rag.loaders.pdf_loader import PDFLoader
from app.rag.models import Chunk
from app.rag.splitters.text_splitter import TextSplitter
from app.rag.embeddings.base import (
    EmbeddingProvider,
)
from app.infrastructure.vectorstore.base import(
    VectorStore,
)

class IngestionService:
    
    def __init__(
        self,
        pdf_loader:PDFLoader,
        text_splitter:TextSplitter,
        embedding_provider:EmbeddingProvider,
        vector_store:VectorStore,
        ) -> None:
        self.pdf_loader = pdf_loader
        self.text_splitter = text_splitter
        self.embedding_provider=embedding_provider
        self.vector_store = vector_store
    def ingest_pdf(
        self,
        file_path:Path,
        document_id:str,
    )->list[Chunk]:
        
        pages = self.pdf_loader.load(file_path)
        
        chunks = self.text_splitter.split(
            pages=pages,
            document_id=document_id,
        )
        
        texts = [
            chunk.text
            for chunk in chunks
        ]
        
        vectors = (
            self.embedding_provider.embed_documents(
                texts=texts
            )
        )
        
        self.vector_store.add(
            chunks=chunks,
            vectors=vectors,
        )
        
        return chunks