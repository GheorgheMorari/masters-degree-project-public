from pydantic import BaseModel


class RagResponseOutput(BaseModel):
    response: str
