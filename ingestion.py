from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings,GoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

def load_documents(dir):
    loader = PyPDFDirectoryLoader(dir)
    docs = loader.load()
    return docs

def chunking(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks

if __name__ == "__main__":
    # loading environment variables
    load_dotenv()
    
    # Initialize vectorstore
    vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
    persist_directory="./.chromadb"
    )
    
    docs = load_documents("documents(pdf)") # Load all documents in the directory(success)
    chunks = chunking(docs) # Split documents into chunks(success)
    vectorstore.add_documents(documents=chunks) # Added vectorstore (success)