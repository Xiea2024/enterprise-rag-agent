from pathlib import Path
from app.rag.loaders.pdf_loader import PDFLoader
from app.rag.models import Chunk
from app.rag.splitters.text_splitter import TextSplitter

class IngestionService:
    
    def __init__(
        self,
        pdf_loader:PDFLoader,
        text_splitter:TextSplitter,
        ) -> None:
        self.pdf_loader = pdf_loader
        self.text_splitter = text_splitter
        
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
        
        return chunks