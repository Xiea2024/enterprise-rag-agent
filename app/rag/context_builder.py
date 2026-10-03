"""
RAG 上下文构建。

属于 RAG 核心层，将检索结果转换为带编号的证据文本，
并生成与证据编号对应的来源信息。
"""

from app.rag.models import (
    RetrievalResult,
    SourceReference,
)

class ContextBuilder:
    """将检索片段整理为 LLM 可读取的上下文。"""

    def build(
            self,
            results:list[RetrievalResult]
    ) -> tuple[str, list[SourceReference]]:
        """返回上下文文本及其来源列表。"""
        context_blocks:list[str] = []
        sources:list[SourceReference]=[]

        for result in results:
            chunk = result.chunk
            text = chunk.text.strip()

            if not text:
                continue

            reference_id = len(sources)+1

            page_label = (
                str(chunk.page_number)
                if chunk.page_number is not None
                else "Unknown"
            )

            context_blocks.append(
                f"[{reference_id}]\n"
                f"文档ID：{chunk.document_id}\n"
                f"页码:{page_label}\n"
                f"内容:\n{text}"
            )

            sources.append(
                SourceReference(
                    reference_id=reference_id,
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    page_number=chunk.page_number,
                    text=text,
                    score=result.score,
                    metadata=chunk.metadata.copy(),
                )
            )

        return "\n\n".join(context_blocks),sources