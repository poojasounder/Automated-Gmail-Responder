from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()
""" text_splitter = SemanticChunker(OpenAIEmbeddings())

docs = text_splitter.create_documents("./Upload_documents/FAQ.pdf")
print(docs[0].page_content) """

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./Upload_documents/FAQ.pdf")
data = loader.load()



