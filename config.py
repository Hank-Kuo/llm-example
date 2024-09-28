import os
from dotenv import load_dotenv

load_dotenv()

class LangfuseConfig:
    secret_key = os.getenv('LANGFUSE_SECRET_KEY')
    public_key = os.getenv('LANGFUSE_PUBLIC_KEY')
    host = os.getenv('LANGFUSE_HOST')

class AzureOpenAIConfig:
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION')
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    model_id = os.getenv('AZURE_OPENAI_MODEL_ID')
    embedding_model = os.getenv('AZURE_OPENAI_EMBEDDING_MODEL')



class Config:
    """The overall configuration of the api."""
    azure_openai= AzureOpenAIConfig()
    langfuse = LangfuseConfig()


print(os.getenv('AZURE_OPENAI_ENDPOINT'))
config = Config()