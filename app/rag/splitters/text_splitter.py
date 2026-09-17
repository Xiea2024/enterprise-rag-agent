from uuid import uuid4

from app.rag.models import Chunk,DocumentPage

class TextSplitter:
    def __init__(
        self,
        chunk_size:int = 1000,
        chunk_overlap:int=200,
    )->None:
        if chunk_size<=0:
            raise ValueError(
                "Chunk size 必须大于 0"
            )
        
        if chunk_overlap<0:
            raise ValueError(
                "Chunk overlap不能为负"
            )
        
        if chunk_overlap>=chunk_size:
            raise ValueError(
                "chunk size 必须比chunk overlap大"
            )
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def split(
        self,
        pages:list[DocumentPage],
        document_id:str,
    )->list[Chunk]:
        chunks:list[Chunk] = []
        chunk_index = 0
        
        for page in pages:
            text = page.text.strip()
            
            if not text:
                continue
            
            start = 0
            
            while start < len(text):
                end = start+self.chunk_size
                
                chunk_text = text[start:end].strip()
                
                if chunk_text:
                    chunks.append(
                        Chunk(
                            id=str(uuid4()),
                            document_id=document_id,
                            chunk_index=chunk_index,
                            text=chunk_text,
                            page_number=page.page_number,
                            metadata=page.metadata.copy(),
                        )
                    )
                    
                    chunk_index+=1
                
                if end>= len(text):
                    break
                
                start = end-self.chunk_overlap
        return chunks
        