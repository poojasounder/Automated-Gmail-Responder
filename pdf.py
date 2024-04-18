import json
import os
import pprint
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

from data import save_documents_json

loader = PyPDFLoader("documents/Bulletin.pdf")
documents = loader.load_and_split()

save_documents_json(documents,"pdf_test.json")