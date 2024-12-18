from pydantic import BaseModel


class RagResponseInput(BaseModel):
    query: str
