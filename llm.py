from langchain_google_vertexai import VertexAI  # type: ignore
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import openai
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader('./documents')
docs = loader.load()

print(len(docs))

