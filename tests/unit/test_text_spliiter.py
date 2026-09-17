from app.rag.models import DocumentPage
from app.rag.splitters.text_splitter import TextSplitter

def test_split_text_with_overlap()->None:
    
    splitter = TextSplitter(
        chunk_size=10,
        chunk_overlap=3,
    )
    
    pages = [
        DocumentPage(
            page_number=1,
            text="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        )
    ]
    
    chunks = splitter.split(
        pages=pages,
        document_id="test-doc",)
    
    assert len(chunks) == 4
    
    assert chunks[0].text == "ABCDEFGHIJ"
    assert chunks[1].text == "HIJKLMNOPQ"

    assert chunks[0].document_id == "test-doc"
    assert chunks[0].page_number == 1
