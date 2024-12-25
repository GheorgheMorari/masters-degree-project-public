from typing import List

from langchain_core.documents import Document


def format_documents(documents: List[Document]) -> str:
    """
    Format a list of documents into a single string.
    """
    return "\n\n".join(doc.page_content for doc in documents)
