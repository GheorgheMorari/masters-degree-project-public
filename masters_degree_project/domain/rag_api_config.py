import os
from typing import Optional

import dotenv
from pydantic import BaseModel

INSIDE_DOCKER = "INSIDE_DOCKER"
OLD_HOST = "localhost"
DOCKER_HOST = "host.docker.internal"

class RagApiConfig(BaseModel):
    OPENAI_API_KEY: str
    OPENAI_API_BASE: str
    OPENAI_MODEL_NAME: Optional[str]
    OPENAI_EMBEDDING_MODEL_NAME: Optional[str]
    OPENAI_MODEL_TEMPERATURE: Optional[float]
    DOCUMENT_SPLIT_CHUNK_SIZE: Optional[int]
    DOCUMENT_SPLIT_CHUNK_OVERLAP: Optional[int]

    @classmethod
    def from_env(cls):
        dotenv.load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

        if not OPENAI_API_KEY or not OPENAI_API_BASE:
            raise ValueError("OPENAI_API_KEY and OPENAI_API_BASE must be set in the environment variables.")

        if os.getenv(INSIDE_DOCKER):
            OPENAI_API_BASE = OPENAI_API_BASE.replace(OLD_HOST, DOCKER_HOST)
            print(f"Env variable:{INSIDE_DOCKER} is set, replacing {OLD_HOST} with {DOCKER_HOST} in OPENAI_API_BASE")
            os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE

        OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
        OPENAI_EMBEDDING_MODEL_NAME = os.getenv("OPENAI_EMBEDDING_MODEL_NAME")
        OPENAI_MODEL_TEMPERATURE = os.getenv("OPENAI_MODEL_TEMPERATURE")
        DOCUMENT_SPLIT_CHUNK_SIZE = os.getenv("DOCUMENT_SPLIT_CHUNK_SIZE")
        DOCUMENT_SPLIT_CHUNK_OVERLAP = os.getenv("DOCUMENT_SPLIT_CHUNK_OVERLAP")

        return cls(OPENAI_API_KEY=OPENAI_API_KEY, OPENAI_API_BASE=OPENAI_API_BASE, OPENAI_MODEL_NAME=OPENAI_MODEL_NAME,
                   OPENAI_EMBEDDING_MODEL_NAME=OPENAI_EMBEDDING_MODEL_NAME,
                   OPENAI_MODEL_TEMPERATURE=float(OPENAI_MODEL_TEMPERATURE) if OPENAI_MODEL_TEMPERATURE else None,
                   DOCUMENT_SPLIT_CHUNK_SIZE=int(DOCUMENT_SPLIT_CHUNK_SIZE) if DOCUMENT_SPLIT_CHUNK_SIZE else None,
                   DOCUMENT_SPLIT_CHUNK_OVERLAP=int(
                       DOCUMENT_SPLIT_CHUNK_OVERLAP) if DOCUMENT_SPLIT_CHUNK_OVERLAP else None)
