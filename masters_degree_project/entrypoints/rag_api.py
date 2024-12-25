from typing import Optional

import bs4
from fastapi import FastAPI
from langchain_core.runnables import RunnableSequence

from masters_degree_project.adapters.custom_openai_embeddings import LLAMA_CPP_Compatible_OpenAIEmbeddings
from masters_degree_project.domain.health_check import DEFAULT_HEALTH_CHECK_ENTRYPOINT_PATH, \
    DEFAULT_HEALTH_CHECK_ENTRYPOINT_PARAMS, HealthCheck
from masters_degree_project.domain.rag_api_config import RagApiConfig
from masters_degree_project.domain.rag_response_input import RagResponseInput
from masters_degree_project.domain.rag_response_output import RagResponseOutput
from masters_degree_project.entrypoints import RAG_RESPONSE_API_ENTRY_POINT_PATH
from masters_degree_project.services.init_rag_chain import init_rag_chain
from masters_degree_project.services.load_documents import load_document_splits_from_web_sources

rag_chain: Optional[RunnableSequence] = None
modified_rag_chain: Optional[RunnableSequence] = None

rag_api_config = RagApiConfig.from_env()

document_splits = load_document_splits_from_web_sources(
    web_paths=["https://lilianweng.github.io/posts/2023-06-23-agent/"],
    bs_kwargs={"parse_only": bs4.SoupStrainer(class_=("post-content", "post-title", "post-header"))},
    split_chunk_size=rag_api_config.DOCUMENT_SPLIT_CHUNK_SIZE,
    split_chunk_overlap=rag_api_config.DOCUMENT_SPLIT_CHUNK_OVERLAP)


def init_rag_api():
    global rag_chain

    rag_chain = init_rag_chain(document_splits, openai_model_name=rag_api_config.OPENAI_MODEL_NAME,
                               openai_model_temperature=rag_api_config.OPENAI_MODEL_TEMPERATURE,
                               embeddings_type=LLAMA_CPP_Compatible_OpenAIEmbeddings,
                               embeddings_kwargs={"model": rag_api_config.OPENAI_EMBEDDING_MODEL_NAME})


app = FastAPI(on_startup=[init_rag_api])


@app.post(RAG_RESPONSE_API_ENTRY_POINT_PATH, response_model=RagResponseOutput)
def route_rag_response(rag_response_input: RagResponseInput) -> RagResponseOutput:
    rag_chain_output = rag_chain.invoke(rag_response_input.query)
    return RagResponseOutput(response=rag_chain_output)


@app.get(DEFAULT_HEALTH_CHECK_ENTRYPOINT_PATH, **DEFAULT_HEALTH_CHECK_ENTRYPOINT_PARAMS)
def route_get_review_localization_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck()
