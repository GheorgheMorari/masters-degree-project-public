from pydantic import BaseModel


class SentenceDecompositionOutput(BaseModel):
    described_action_or_behavior: str
    described_detailed_subject: str
