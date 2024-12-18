from enum import Enum
from http import HTTPStatus

from pydantic import BaseModel


class HealthCheckStatus(str, Enum):
    OK = "OK"
    FAIL = "FAIL"


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: HealthCheckStatus = HealthCheckStatus.OK


DEFAULT_HEALTH_CHECK_ENTRYPOINT_PATH = "/healthcheck"
DEFAULT_HEALTH_CHECK_ENTRYPOINT_PARAMS = {"tags": ["healthcheck"],
                                          "summary": "Perform a Health Check",
                                          "response_description": "Return HTTP Status Code 200 (OK)",
                                          "status_code": HTTPStatus.OK,
                                          "response_model": HealthCheck}
