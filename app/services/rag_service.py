"""
RAG 问答业务编排。

属于 Service 层，串联检索、上下文构建、提示词构建
和 LLM 生成，并返回答案及来源信息。
"""

from app.rag.context_builder import ContextBuilder
from app.rag.llms.base import LLMProvider
from app.rag.models import RAGResponse
from app.rag.prompt_builder import PromptBuilder
from app.services.retrieval_service import RetrievalService


class RAGService:
    """编排一次完整的 RAG 问答流程。"""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        llm_provider: LLMProvider,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.llm_provider = llm_provider

    def ask(
        self,
        query: str,
        top_k: int = 5,
    ) -> RAGResponse:
        """检索相关资料，并生成带来源信息的回答。"""
        query = query.strip()

        if not query:
            raise ValueError("问题不能为空")

        if top_k <= 0:
            raise ValueError("top_k 必须大于 0")

        results = self.retrieval_service.retrieve(
            query=query,
            top_k=top_k,
        )

        context, sources = self.context_builder.build(
            results=results,
        )

        # 没有可用文本时直接返回，避免无依据地调用模型。
        if not sources:
            return RAGResponse(
                answer="未检索到可用资料，无法根据知识库回答。",
                sources=[],
            )

        system_prompt, user_prompt = (
            self.prompt_builder.build(
                query=query,
                context=context,
            )
        )

        answer = self.llm_provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        ).strip()

        if not answer:
            raise ValueError("LLM 返回了空回答")

        return RAGResponse(
            answer=answer,
            sources=sources,
        )