from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain.schema import Document
import json
SCRAPED_DATA = "cs-website-scraped/scraped_data.json"
def remove_css(documents):
    """Removes css and pdf files from Documents list"""
    extensions_removed = []

    for doc in documents:
        source = doc.metadata['source']
        add = True
        for extension in ".css":
            if source.endswith(extension):
                add = False
        if add:
            extensions_removed.append(doc)

    return extensions_removed
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
    documents = remove_css(documents)
    save_documents_json(documents, SCRAPED_DATA)
    return documents


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
    
    # Scrape sites
    website = "https://pdx.edu/computer-science/"
    scraped_data = scrape(website, 4)
    vectorstore.add_documents(documents=scraped_data) # Added vectorstore of cs_website(success)