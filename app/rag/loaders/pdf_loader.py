from pathlib import Path
from pypdf import PdfReader
from app.rag.models import DocumentPage

class PDFLoader:
    
    def Load(
        self,
        file_path:Path,
    )->list[DocumentPage]:
        
        if not file_path.exists():
            raise FileNotFoundError(
                f"PDF file not found : {file_path}"
            )
        reader = PdfReader(file_path)
        
        pages:list[DocumentPage] = []
        
        for index,page in enumerate(reader.pages):
            text = page.extract_text() or ""
            
            #空文本跳过
            if not text.strip():
                continue
            
            pages.append(
                DocumentPage(
                    page_number = index+1,
                    text=text,
                    metadata={
                        "source":file_path.name,
                    },
                )
            )
        return pages