from fastapi import FastAPI

from masters_degree_project.domain.health_check import DEFAULT_HEALTH_CHECK_ENTRYPOINT_PATH, \
    DEFAULT_HEALTH_CHECK_ENTRYPOINT_PARAMS, HealthCheck
from masters_degree_project.domain.rag_response_input import RagResponseInput
from masters_degree_project.domain.rag_response_output import RagResponseOutput
from masters_degree_project.entrypoints import RAG_RESPONSE_API_ENTRY_POINT_PATH


def init_rag():
    pass


app = FastAPI(on_startup=[init_rag])


@app.post(RAG_RESPONSE_API_ENTRY_POINT_PATH, response_model=RagResponseOutput)
def route_rag_response(rag_response_input: RagResponseInput) -> RagResponseOutput:
    return RagResponseOutput(response="This is a test response")


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
