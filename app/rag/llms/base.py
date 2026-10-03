"""
LLM Provider 抽象。

属于 RAG 核心抽象层，定义文本生成接口，
使业务流程可以独立于具体 LLM SDK 和服务实现。
"""

from abc import ABC,abstractmethod

class LLMProvider(ABC):
    """定义 RAG 生成阶段需要的 LLM 能力。"""

    @abstractmethod
    def generate(
        self,
        system_prompt:str,
        user_prompt:str,
    )->str:
        """根据系统指令和用户提示词生成回答。"""
        raise NotImplementedError