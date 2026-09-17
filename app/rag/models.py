from pydantic import BaseModel,Field

class DocumentPage(BaseModel):
    page_number:int
    text:str
    metadata:dict[str,str] = Field(default_factory=dict)
    

class Chunk(BaseModel):
    id:str
    document_id:str
    chunk_index:int
    text:str
    
    page_number:int |None = None
    
    metadata: dict[str,str] = Field(default_factory=dict)