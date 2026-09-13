from abc import ABC,abstractmethod
from typing import Any

class BaseAgent(ABC):
    
    @property
    @abstractmethod
    def name(self)->str:
        pass
    
    @abstractmethod
    async def run(
        self,
        input_data:Any,
    )->Any:
        pass