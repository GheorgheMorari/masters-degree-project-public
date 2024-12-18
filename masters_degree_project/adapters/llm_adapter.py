import os
from typing import Optional, Type, List, Dict, TypeVar

import instructor
import openai
from pydantic import BaseModel

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)

BASE_LLM_ADAPTER_DEFAULT_TEMPERATURE = 0.1
BASE_LLM_ADAPTER_DEFAULT_STOP_TOKENS = ("<|end|>",)
BASE_LLM_ADAPTER_ROLE_KEY = "role"
BASE_LLM_ADAPTER_CONTENT_KEY = "content"
BASE_LLM_ADAPTER_USER_ROLE = "user"
BASE_LLM_ADAPTER_SYSTEM_ROLE = "system"
BASE_LLM_ADAPTER_ASSISTANT_ROLE = "assistant"
BASE_LLM_ADAPTER_MAX_RETRIES = 5


class LLMAdapterException(Exception):
    pass


class LLMAdapterInvalidCredentialsException(LLMAdapterException):
    pass


class LLMAdapterConnectionErrorException(LLMAdapterException):
    pass


class LLMAdapter:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, model_name: Optional[str] = None):
        if base_url is None:
            base_url = os.environ["LLM_SERVER_API_BASE_URL"]
        if api_key is None:
            api_key = os.environ["LLM_SERVER_API_KEY"]
        if model_name is None:
            model_name = os.environ["LLM_SERVER_API_MODEL_NAME"]

        self.model_name = model_name

        self.openai_client = openai.OpenAI(base_url=base_url, api_key=api_key)

        self.instructor_client = instructor.from_openai(self.openai_client)

    def generate_chat_result(self, messages: List[Dict[str, str]], response_model: Type[BaseModelType],
                             temperature: Optional[float] = BASE_LLM_ADAPTER_DEFAULT_TEMPERATURE,
                             stop_tokens: Optional[List[str]] = BASE_LLM_ADAPTER_DEFAULT_STOP_TOKENS) -> BaseModelType:
        try:
            return self.instructor_client.completions.create(model=self.model_name, response_model=response_model,
                                                             messages=messages, temperature=temperature,
                                                             stop=stop_tokens, max_retries=BASE_LLM_ADAPTER_MAX_RETRIES)
        except (openai.APIConnectionError, openai.APITimeoutError) as connection_error_exception:
            raise LLMAdapterConnectionErrorException(connection_error_exception)
        except openai.AuthenticationError as exception:
            raise LLMAdapterInvalidCredentialsException(exception)
        except Exception as exception:
            raise LLMAdapterException(exception)

    def generate_instruct_result(self, instruction: str, response_model: Type[BaseModelType],
                                 temperature: Optional[float] = BASE_LLM_ADAPTER_DEFAULT_TEMPERATURE,
                                 stop_tokens: Optional[
                                     List[str]] = BASE_LLM_ADAPTER_DEFAULT_STOP_TOKENS) -> BaseModelType:
        return self.generate_chat_result(messages=[
            {BASE_LLM_ADAPTER_ROLE_KEY: BASE_LLM_ADAPTER_USER_ROLE, BASE_LLM_ADAPTER_CONTENT_KEY: instruction}],
            response_model=response_model, temperature=temperature, stop_tokens=stop_tokens)
