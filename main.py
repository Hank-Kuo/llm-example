from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.text_splitter import CharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langfuse import Langfuse

from config import config
from document from DOCUMENTS

llm = AzureChatOpenAI(
    azure_endpoint=config.azure_openai.endpoint,
    azure_deployment=config.azure_openai.deployment,
    openai_api_version=config.azure_openai.api_version,
    openai_api_key=config.azure_openai.api_key,
    model=config.azure_openai.model_id,
    temperature=0,
)


embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=256,
    azure_endpoint=config.azure_openai.endpoint
    api_key=config.azure_openai.api_key,
    openai_api_version=config.azure_openai.api_version
)

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Answer the user\'s questions in Chinese, based on the context provided below:\n\n{context}'),
    ('user', 'Question: {input}'),
])

docs = [ Document(page_content=d) for d in DOCUMENTS]

text_splitter = CharacterTextSplitter(chunk_size=20, chunk_overlap=5)
documents = text_splitter.split_documents(docs)