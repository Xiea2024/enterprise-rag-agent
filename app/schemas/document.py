from enum import Enum

from pydantic import BaseModel

class DocumentStatus(str,Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


class DocumentResponse(BaseModel):
    id:str
    filename:str
    content_type:str|None
    status:DocumentStatus
    storage_path:str|None = None