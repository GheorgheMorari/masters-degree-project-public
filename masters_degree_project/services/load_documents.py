from typing import List, Optional

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_document_splits_from_web_sources(web_paths: List[str], bs_kwargs: Optional[dict] = None,
                                          split_chunk_size: int = 400, split_chunk_overlap: int = 100) -> List[
    Document]:
    """
    Load documents from web sources.
    """
    loader = WebBaseLoader(web_paths=web_paths, bs_kwargs=bs_kwargs)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=split_chunk_size, chunk_overlap=split_chunk_overlap)
    return text_splitter.split_documents(docs)
