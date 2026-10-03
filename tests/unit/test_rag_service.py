"""
RAGService 单元测试。

属于测试层，通过 Mock 隔离检索与 LLM，
验证正常问答以及没有资料时的业务行为。
"""

from unittest.mock import Mock

from app.rag.context_builder import ContextBuilder
from app.rag.llms.base import LLMProvider
from app.rag.models import Chunk, RetrievalResult
from app.rag.prompt_builder import PromptBuilder
from app.services.rag_service import RAGService
from app.services.retrieval_service import RetrievalService


def test_ask_returns_answer_and_sources() -> None:
    """有检索资料时，将证据传给模型并返回答案和来源。"""
    # spec 限制 Mock 的可用属性，避免使用不存在的方法。
    retrieval = Mock(spec=RetrievalService)
    llm = Mock(spec=LLMProvider)

    retrieval.retrieve.return_value = [
        RetrievalResult(
            chunk=Chunk(
                id="chunk-1",
                document_id="document-1",
                chunk_index=0,
                text="员工每年享有 10 天年假。",
                page_number=3,
            ),
            score=0.9,
        )
    ]
    llm.generate.return_value = "员工每年享有 10 天年假。[1]"

    service = RAGService(
        retrieval_service=retrieval,
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        llm_provider=llm,
    )

    response = service.ask("年假有多少天？")

    assert response.answer == "员工每年享有 10 天年假。[1]"
    assert len(response.sources) == 1
    assert response.sources[0].document_id == "document-1"
    assert response.sources[0].page_number == 3
    assert response.sources[0].reference_id == 1

    retrieval.retrieve.assert_called_once_with(
        query="年假有多少天？",
        top_k=5,
    )
    llm.generate.assert_called_once()

    # 检查模型实际收到的内容，避免只验证预设答案。
    user_prompt = llm.generate.call_args.kwargs["user_prompt"]
    assert "年假有多少天？" in user_prompt
    assert "员工每年享有 10 天年假。" in user_prompt
    assert "[1]" in user_prompt


def test_ask_without_sources_skips_llm() -> None:
    """未检索到资料时，直接返回，不调用模型。"""
    retrieval = Mock(spec=RetrievalService)
    llm = Mock(spec=LLMProvider)
    retrieval.retrieve.return_value = []

    service = RAGService(
        retrieval_service=retrieval,
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        llm_provider=llm,
    )

    response = service.ask("年假有多少天？")

    assert response.sources == []
    assert "无法根据知识库回答" in response.answer
    llm.generate.assert_not_called()