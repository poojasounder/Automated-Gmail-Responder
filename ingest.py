import os
from scrape import *
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

INDEX = "faiss_index"

def files(path):
    """Returns filenames in given path"""
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def create_faiss():
    """Creates a FAISS vectorstore and saves it to disk"""
    documents = load_documents_json(SCRAPED_DATA)
    db = FAISS.from_documents(documents, embeddings)
    for file_name in files("documents/"):
        path = f"documents/{file_name}"
        _, file_type = os.path.splitext(path)
        if file_type == ".pdf":
            loader = PyPDFLoader(path)
            pages = loader.load_and_split()
            db.add_documents(pages)
    db.save_local(INDEX)