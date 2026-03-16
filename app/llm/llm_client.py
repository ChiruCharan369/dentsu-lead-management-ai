import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings

_ = load_dotenv(find_dotenv())

AZURE_OPENAI_HEADERS = {
    "x-service-line": os.getenv("SERVICE_LINE"),
    "x-brand": os.getenv("BRAND"),
    "x-project": os.getenv("PROJECT"),
    "api-version": os.getenv("API_VERSION"),
    # "api-version": os.getenv("OPENAI_API_VERSION"),
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
}

# OPENAI_GPT3_KEY = os.environ["GPT3.5_KEY"]
# OPENAI_GPT4_KEY = os.environ["GPT4_KEY"]
# OPENAI_GPT4_1_KEY = os.environ["GPT4_1_KEY"]

OPENAI_GPT3_KEY = os.getenv("GPT3.5_KEY")
OPENAI_GPT4_KEY = os.getenv("GPT4_KEY")
OPENAI_GPT4_1_KEY = os.getenv("GPT4_1_KEY")


def llm_gpt4o1():
    """
    Initialize and return an AzureChatOpenAI instance for GPT-4o.
    """
    headers = AZURE_OPENAI_HEADERS
    # headers["Ocp-Apim-Subscription-Key"] = OPENAI_GPT4_1_KEY
    headers["Ocp-Apim-Subscription-Key"] = os.getenv("GPT4_1_KEY")
    return AzureChatOpenAI(
        deployment_name="gpt-4.1-nano",
        model_name="gpt-4.1-nano",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        default_headers=headers,
        seed=42,
        temperature=0.0,
        cache=False,
    )

def llm_gpt4o():
    """
    Initialize and return an AzureChatOpenAI instance for GPT-4o.
    """
    headers = AZURE_OPENAI_HEADERS
    # headers["Ocp-Apim-Subscription-Key"] = OPENAI_GPT4_KEY
    headers["Ocp-Apim-Subscription-Key"] = os.getenv("GPT4_KEY")
    return AzureChatOpenAI(
        deployment_name="GPT4o128k",
        model_name="GPT4o128k",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        default_headers=headers,
        seed=42,
        temperature=0.0,
        cache=False,
    )

def azure_embeddings():
    """
    Initialize Azure OpenAI Embeddings (TextEmbeddingAda2).
    Used for semantic similarity (curated example selection, etc.)
    """
    headers = AZURE_OPENAI_HEADERS
    headers["Ocp-Apim-Subscription-Key"] = os.getenv("GPT3.5_KEY")
    # headers["Ocp-Apim-Subscription-Key"] = OPENAI_GPT3_KEY
    return AzureOpenAIEmbeddings(
        model="TextEmbeddingAda2",
        api_key=os.getenv("GPT3.5_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        default_headers=headers,
    )


def invoke_llm(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content

llm = llm_gpt4o1()