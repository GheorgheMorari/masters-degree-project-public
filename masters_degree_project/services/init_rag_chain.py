from typing import List, Type, Optional

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from masters_degree_project.services.format_documents import format_documents

RAG_CHAIN_PROMPT = ChatPromptTemplate.from_messages([("human", """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question}
Context: {context}
Answer:"""), ])
DEFAULT_OPENAI_MODEL_NAME = "gpt-3.5-turbo"
DEFAULT_OPENAI_MODEL_TEMPERATURE = 0.0


def init_rag_chain(document_splits: List[Document], openai_model_name: str = DEFAULT_OPENAI_MODEL_NAME,
                   openai_model_temperature: float = DEFAULT_OPENAI_MODEL_TEMPERATURE,
                   embeddings_type: Type[Embeddings] = OpenAIEmbeddings,
                   embeddings_kwargs: Optional[dict] = None) -> RunnableSequence:
    """
    Initialize a RAG chain runnable sequence with a given set of documents and an OpenAI model.
    """

    vectorstore = FAISS.from_documents(documents=document_splits,
                                       embedding=embeddings_type(**(embeddings_kwargs or {})))
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model_name=openai_model_name, temperature=openai_model_temperature)

    return ({"context": retriever | format_documents,
             "question": RunnablePassthrough()} | RAG_CHAIN_PROMPT | llm | StrOutputParser())
