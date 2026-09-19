from pathlib import Path

from app.core.config import get_settings
from app.infrastructure.embeddings.sentence_transformer import(
    SentenceTransformerEmbedding,
)

from app.infrastructure.vectorstore.qdrant import(
    QdrantVectorStore,
)

from app.rag.loaders.pdf_loader import PDFLoader
from app.rag.splitters.text_splitter import TextSplitter
from app.services.ingestion_service import (
    IngestionService,
)

settings = get_settings()

embedding = SentenceTransformerEmbedding(
    model_name=settings.embedding_model,
)

vector_store = QdrantVectorStore(
    url = settings.qdrant_url,
    collection_name=settings.qdrant_collection,
    vector_size=embedding.dimension,
)

service = IngestionService(
    pdf_loader=PDFLoader(),
    text_splitter=TextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    ),
    embedding_provider=embedding,
    vector_store=vector_store,
)

chunks = service.ingest_pdf(
    file_path=Path("data/uploads/test.pdf"),
    document_id="test-document",
)

print(f"Ingested {len(chunks)} chunks")

