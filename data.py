import json, os, pprint, re
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, AsyncHtmlLoader, AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.schema import Document

SCRAPED_DATA = "documents/scraped_data.json"
PERSIST = "./.chromadb"

def files(path):
    """Returns filenames in given path"""
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def save_documents_json(documents, filename):
    """Saves list of Documents as JSON file"""
    data = [doc.dict() for doc in documents]
    with open(filename, 'w+') as f:
        json.dump(data, f)

def load_documents_json(filename):
    """Reads a JSON file and returns a list of Documents"""
    with open(filename, 'r') as f:
        data: list = json.load(f)
    return [Document(**doc_dict) for doc_dict in data]

def clean_text(text):
    """Extracts alphanumeric characters and cleans extra whitespace"""
    # Remove apostraphes
    #text = re.sub(r"['’]", "", text)
    # Replace special characters with spaces
    #text = re.sub(r'[^\w\s]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def clean_documents(documents):
    """Cleans page_content text of Documents list"""
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

def scrape(filename):
    """Scrapes URLs in given file and returns Documents"""
    # Creates list of URLs
    with open(filename, 'r') as file:
        sites = [line.rstrip('\n') for line in file]

    # Scrapes list of sites
    loader = AsyncChromiumLoader(sites)
    loader.requests_kwargs = {'verify': False}
    docs = loader.load()
    # Extract article tag
    transformer = BeautifulSoupTransformer()
    docs_tr = transformer.transform_documents(
        documents=docs,
        tags_to_extract=['article']
    )

    return docs_tr

# Scrape sites
file = "urls.txt"
documents = scrape(file)
clean_documents(documents)
save_documents_json(documents, SCRAPED_DATA)
scraped_data = load_documents_json(SCRAPED_DATA)

"""
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10000,
    chunk_overlap=1000,
    length_function=len
)

vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
    persist_directory=PERSIST
)
"""