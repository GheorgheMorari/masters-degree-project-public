from typing import List, Optional

from langchain_openai import OpenAIEmbeddings


class LLAMA_CPP_Compatible_OpenAIEmbeddings(OpenAIEmbeddings):
    """
    OpenAIEmbeddings adapter for LLAMA CPP compatibility.
    This adapter removes the pretokenization step and uses the OpenAI API
    """

    def _get_len_safe_embeddings(
            self, texts: List[str], *, engine: str, chunk_size: Optional[int] = None
    ) -> List[List[float]]:
        """
        Generate length-safe embeddings for a list of texts.

        This method handles tokenization and embedding generation, respecting the
        set embedding context length and chunk size. It supports both tiktoken
        and HuggingFace tokenizer based on the tiktoken_enabled flag.

        Args:
            texts (List[str]): A list of texts to embed.
            engine (str): The engine or model to use for embeddings.
            chunk_size (Optional[int]): The size of chunks for processing embeddings.

        Returns:
            List[List[float]]: A list of embeddings for each input text.
        """
        _chunk_size = chunk_size or self.chunk_size
        # _iter, tokens, indices = self._tokenize(texts, _chunk_size)
        batched_embeddings: List[List[float]] = []
        # for i in _iter:
        response = self.client.create(
            input=texts, **self._invocation_params
        )
        if not isinstance(response, dict):
            response = response.model_dump()
        # responses = [self.client.create(input=text, **self._invocation_params) for text in texts]
        batched_embeddings.extend(r["embedding"] for r in response["data"])

        # embeddings = _process_batched_chunked_embeddings(
        #     len(texts), tokens, batched_embeddings, indices, self.skip_empty
        # )
        embeddings = batched_embeddings

        _cached_empty_embedding: Optional[List[float]] = None

        def empty_embedding() -> List[float]:
            nonlocal _cached_empty_embedding
            if _cached_empty_embedding is None:
                average_embedded = self.client.create(
                    input="", **self._invocation_params
                )
                if not isinstance(average_embedded, dict):
                    average_embedded = average_embedded.model_dump()
                _cached_empty_embedding = average_embedded["data"][0]["embedding"]
            return _cached_empty_embedding

        return [e if e is not None else empty_embedding() for e in embeddings]
