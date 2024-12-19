from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from tqdm import tqdm

from masters_degree_project.adapters.llm_adapter import LLMAdapter
from masters_degree_project.services.behaviour_indexing import behaviour_indexing


class BehaviourIndexingEmbeddings(Embeddings):

    def __init__(self, llm_adapter: LLMAdapter, openai_embeddings: OpenAIEmbeddings):
        self.llm_adapter = llm_adapter
        self.openai_embeddings = openai_embeddings

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        modified_texts = [behaviour_indexing(text, self.llm_adapter) for text in tqdm(texts)]
        return self.openai_embeddings.embed_documents(modified_texts)

    def embed_query(self, text: str) -> list[float]:
        return self.openai_embeddings.embed_query(behaviour_indexing(text, self.llm_adapter))
