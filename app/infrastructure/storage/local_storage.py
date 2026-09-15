from pathlib import Path

import aiofiles
from fastapi import UploadFile

class LocalStorage:
    
    def __init__(self,base_path:str = "data/uploads")->None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(
            parents=True,
            exist_ok=True
        )
        
    async def save(
        self,
        document_id:str,
        file:UploadFile,
    )->Path:
        filename = file.filename or "unknown"
        safename = Path(filename).name
        
        target_path = self.base_path / (
            f"{document_id}_{safename}"
        )
        async with aiofiles.open(
            target_path,
            "wb",
        ) as output_file:
            while chunk := await file.read(1024*1024):
                await output_file.write(chunk)
        
        return target_path