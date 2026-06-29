import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv, find_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

_ = load_dotenv(find_dotenv())

AZURE_OPENAI_HEADERS = {
    "x-service-line": os.getenv("SERVICE_LINE"),
    "x-brand": os.getenv("BRAND"),
    "x-project": os.getenv("PROJECT"),
    "api-version": os.getenv("API_VERSION"),
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
}


def _get_api_keys() -> List[str]:
    keys: List[str] = []
    for index in range(1, 6):
        for var_name in (f"OPEN_KEY_{index}", f"open_key_{index}"):
            key = os.getenv(var_name)
            if key and key.strip():
                keys.append(key.strip())
                break

    if not keys:
        for var_name in ("OPENAI_API_KEY", "AZURE_OPENAI_API_KEY"):
            legacy_key = os.getenv(var_name)
            if legacy_key and legacy_key.strip():
                keys.append(legacy_key.strip())
                break

    return keys


API_KEYS = _get_api_keys()


def _get_headers(api_key: Optional[str] = None) -> Dict[str, Any]:
    headers = dict(AZURE_OPENAI_HEADERS)
    if api_key:
        headers["Ocp-Apim-Subscription-Key"] = api_key
    return headers


class FallbackAzureChat:
    def __init__(self, deployment_name: str, model_name: str, api_keys: Optional[List[str]] = None, bind_kwargs: Optional[Dict[str, Any]] = None):
        self.deployment_name = deployment_name
        self.model_name = model_name
        self.api_keys = api_keys or API_KEYS
        self.bind_kwargs = bind_kwargs or {}

    def _build_client(self, api_key: str) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            deployment_name=self.deployment_name,
            model_name=self.model_name,
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            api_key=api_key,
            default_headers=_get_headers(api_key),
            seed=42,
            temperature=0.0,
            cache=False,
        )

    def invoke(self, prompt: str, **kwargs: Any) -> Any:
        last_error: Optional[Exception] = None
        for api_key in self.api_keys:
            try:
                client = self._build_client(api_key)
                if self.bind_kwargs:
                    client = client.bind(**self.bind_kwargs)
                return client.invoke(prompt, **kwargs)
            except Exception as exc:
                last_error = exc

        if last_error is not None:
            raise last_error
        raise RuntimeError("No Azure OpenAI API keys configured")

    def bind(self, **kwargs: Any) -> "FallbackAzureChat":
        return FallbackAzureChat(self.deployment_name, self.model_name, self.api_keys, {**self.bind_kwargs, **kwargs})


def llm_gpt4o1():
    """
    Initialize and return a fallback AzureChatOpenAI wrapper for GPT-4.1.
    """
    return FallbackAzureChat(deployment_name="gpt-4.1-nano", model_name="gpt-4.1-nano")


def llm_gpt4o():
    """
    Initialize and return a fallback AzureChatOpenAI wrapper for GPT-4o.
    """
    return FallbackAzureChat(deployment_name="GPT4o128k", model_name="GPT4o128k")


def azure_embeddings():
    """
    Initialize Azure OpenAI Embeddings (TextEmbeddingAda2).
    Used for semantic similarity (curated example selection, etc.)
    """
    for api_key in API_KEYS:
        try:
            return AzureOpenAIEmbeddings(
                model="TextEmbeddingAda2",
                api_key=api_key,
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_version=os.getenv("OPENAI_API_VERSION"),
                default_headers=_get_headers(api_key),
            )
        except Exception:
            continue

    raise RuntimeError("No Azure OpenAI API keys configured")


def invoke_llm(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content


llm = llm_gpt4o1()