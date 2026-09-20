from app.core.config import get_settings

from app.infrastructure.embeddings.sentence_transformer import(
    SentenceTransformerEmbedding,
)

from app.infrastructure.vectorstore.qdrant import (
    QdrantVectorStore,
)

from app.services.retrieval_service import(
    RetrievalService,
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

retrieval_service = RetrievalService(
    embedding_provider=embedding,
    vector_store=vector_store,
)

query = input("Question:")

results = retrieval_service.retrieve(
    query=query,
    top_k=5,
)

print("\n Retrieval Result\n")

for index,result in enumerate(
    results,
    start=1,
):
    print(
        f"--- Result {index} ---"
    )

    print(
        f"Score: {result.score:.4f}"
    )
    
    print(
        f"Document: "
        f"{result.chunk.document_id}"
    )

    print(
        f"Page: "
        f"{result.chunk.page_number}"
    )

    print(
        result.chunk.text
    )

    print()