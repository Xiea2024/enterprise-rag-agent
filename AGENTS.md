# Enterprise RAG Agent - Development Instructions

## 项目目标

本项目是一个面向企业知识库场景的 RAG + AI Agent 系统。

当前阶段优先构建清晰、可测试、可扩展的后端架构，
而不是追求快速堆砌功能。

## Architecture

主要分层：

- `app/api`: FastAPI API 层
- `app/services`: Application / Service 层
- `app/rag`: RAG 核心抽象与 Pipeline
- `app/agents`: Agent 抽象与编排
- `app/repositories`: Repository 层
- `app/infrastructure`: 外部基础设施实现
- `app/schemas`: API / DTO 数据结构
- `app/core`: 配置、日志等基础能力

依赖方向应尽量保持：

API
→ Service
→ Abstraction
→ Infrastructure

业务层不要直接依赖具体 Provider。

## Python Code Style

所有 Python 文件必须：

1. 文件顶部包含中文 Module Docstring。
2. Module Docstring 说明：
   - 文件职责
   - 所属架构层
   - 主要用途
3. Class 和重要 public method 应包含中文 Docstring。
4. 关键业务逻辑和非直观设计必须添加中文注释。
5. 不需要对显而易见的代码逐行注释。

以下专业术语可以保留英文：

- RAG
- LLM
- Embedding
- VectorStore
- Provider
- Repository
- Pipeline
- Context
- Prompt
- Reranker
- Agent

## Engineering Principles

- FastAPI Route 不直接访问 Qdrant。
- Service 不直接依赖具体 LLM SDK。
- RAG Pipeline 不绑定具体 Embedding Provider。
- 优先通过 abstraction/interface 解耦 Infrastructure。
- Unit Test 不应该依赖真实 Qdrant、LLM API 或远程服务。
- Integration Test 可以使用真实 Infrastructure。
- 不要为了使用框架而引入 LangChain/LangGraph。
- 新增依赖前说明引入理由。

## Development Workflow

项目使用：

- Python 3.12
- uv
- pytest
- FastAPI
- Qdrant
- Docker Compose

安装依赖：

    uv sync

运行测试：

    uv run pytest -v

启动 Infrastructure：

    docker compose up -d

## Current Development Stage

当前已经完成：

- FastAPI foundation
- Document upload
- PDF Loader
- Text Splitter
- Embedding Provider
- Qdrant VectorStore
- Ingestion Pipeline
- Semantic Retrieval

当前正在开发：

- RAG Generation Pipeline

下一阶段：

- Context Builder
- Prompt Builder
- LLM Provider
- RAGService
- Reranker
- Retrieval Quality
- Chat API
- Agent
- Multi-Agent

## Important

不要在没有明确要求的情况下大规模重构整个项目。

修改代码前先理解现有架构。

优先进行小规模、可验证的修改。

不要删除现有 abstraction，除非有明确的架构理由。