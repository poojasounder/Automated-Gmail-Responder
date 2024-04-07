import json
import os
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.schema import Document
# from langchain_community.embeddings import HuggingFaceEmbeddings

# Definitely don't want CSS file but might find a way to use PDF files
REMOVE_SITES = [".css", ".pdf"]
MAX_DEPTH = 4
SCRAPED_DATA = "documents/scraped_data.json"
INDEX = "faiss_index"

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

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

def extract_text(html):
    """Used by RecursiveURLLoader to extract text"""
    soup = BeautifulSoup(html, "html.parser")
    article_tag = soup.find("article")
    if article_tag:
        return article_tag.get_text(' ', strip=True)
    div_contents = soup.find("div", id="contents")
    if div_contents:
         return div_contents.get_text(' ', strip=True)
    return ' '.join(soup.stripped_strings)

def remove_css_and_pdf(documents):
    """Removes css and pdf files from Documents list"""
    extensions_removed = []

    for doc in documents:
        source = doc.metadata['source']
        add = True
        for extension in REMOVE_SITES:
            if source.endswith(extension):
                add = False
        if add:
            print(source)
            extensions_removed.append(doc)

    return extensions_removed 

def scrape(url, max_depth):
    """Scrapes given URL and returns list of Document objects"""
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=max_depth,
        timeout=15,
        prevent_outside=True,
        check_response_status=True,
        extractor=extract_text
    )

    documents = loader.load()
    documents = remove_css_and_pdf(documents)
    save_documents_json(documents, SCRAPED_DATA)

    return documents

# This function probably works, haven't tested because FAISS giving weird results for now
def create_faiss(scraped_data):
    """Initializes FAISS with scraped data, ingests pdf files, saves FAISS to disk"""
    documents = load_documents_json(scraped_data)
    db = FAISS.from_documents(documents, embeddings)
    for file_name in files("documents/"):
        path = f"documents/{file_name}"
        _, file_type = os.path.splitext(path)
        if file_type == ".pdf":
            loader = PyPDFLoader(path)
            pages = loader.load_and_split()
            db.add_documents(pages)
    db.save_local(INDEX)

# Scrape sites
website = "https://pdx.edu/computer-science/"
scraped_data = scrape(website, MAX_DEPTH)
print("Number of pages:", len(scraped_data))

# Create FAISS
db = FAISS.from_documents(scraped_data, embeddings)
print("FAISS created")

# Save FAISS to disk
db.save_local(INDEX)
print("FAISS saved")

# Load FAISS from disk
vector_store = FAISS.load_local(INDEX, embeddings, allow_dangerous_deserialization=True)
print("FAISS loaded")

# Sanity check with similarity_search
query = "What is the University Coronavirus response?"
docs = vector_store.similarity_search(query, k=3)
print(docs)
print("Number of docs:", len(docs))

# Was going to copy code from test.py in Pooja's data-new branch
# but sanity check is failing when number of documents increases

# Example:
# Asking "What is the University coronavirus response?" works when ingesting 10 web pages but not 40