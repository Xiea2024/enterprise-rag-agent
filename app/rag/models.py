"""
RAG 核心数据模型。

属于 RAG 核心层，定义文档页面、文本片段、
检索结果以及生成回答所需的数据结构。
"""
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
    
class RetrievalResult(BaseModel):
    chunk:Chunk
    score:float

class SourceReference(BaseModel):
     """表示用于回答的证据片段及其来源信息。"""

     reference_id:int
     chunk_id:str
     document_id:str
     page_number:int|None = None
     text:str
     score:float
     metadata:dict[str,str]=Field(default_factory=dict)

class RAGResponse(BaseModel):
    """表示 RAG 返回的答案及提供给模型的来源。"""

    answer:str
    sources:list[SourceReference] = Field(
        default_factory=list
    )