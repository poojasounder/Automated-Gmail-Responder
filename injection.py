from urllib.parse import urljoin
from langchain_community.document_loaders import PyPDFDirectoryLoader, AsyncChromiumLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import re, json
import requests
from bs4 import BeautifulSoup
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings

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
    # Filter out anchor tags that do not start with 'https'
    for doc in docs:
        soup = BeautifulSoup(doc.page_content, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if not href.startswith("https"):
                link.decompose()  # Remove the anchor tag if href does not start with 'https'

        # Update the content of the document
        doc.page_content = str(soup)
    # Extract article tag
    transformer = BeautifulSoupTransformer()
    docs_tr = transformer.transform_documents(
        documents=docs,
        tags_to_extract=['article']
    )
    
    return docs_tr

def load_pdf_documents(dir):
    loader = PyPDFDirectoryLoader(dir)
    docs = loader.load()
    return docs

def chunking(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=2000)
    chunks = text_splitter.split_documents(documents)
    return chunks

def extract_text(html):
    """Used by loader to extract text from div tag with id of main"""
    soup = BeautifulSoup(html, "html.parser")
    div_main = soup.find("div", {"id": "main"})
    if div_main:
        return div_main.get_text(" ", strip=True)
    return " ".join(soup.stripped_strings)

def scrape_recursive(url, depth):
    """Recursively scrapes URL and returns Documents"""
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=depth,
        timeout=20,
        use_async=True,
        prevent_outside=True,
        check_response_status=True,
        continue_on_failure=True,
        extractor=extract_text,
    )
    docs = loader.load()
    clean_documents(docs)
    return docs
""" # create embeddings using OpenAIEmbeddings() and save them in a Chroma vector store 
def create_embeddings(chunks): 
	embeddings = OpenAIEmbeddings()

	# if you want to use a specific directory for chromadb 
	vector_store = Chroma.from_documents(chunks, embeddings, persist_directory='./chroma_db') 
	return vector_store """
if __name__ == "__main__":
    # loading environment variables
    load_dotenv()
    
    # Initialize vectorstore
    vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./.chromadb"
    )
    
    # Gets all the relevent URL's from the CS department and adds it to url.txt file
    response = requests.get("https://www.pdx.edu/computer-science/")
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    # Open a file in write mode
    with open("./urls.txt", "w") as file:
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'computer-science' in href:
                full_url = urljoin("https://www.pdx.edu/computer-science/", href)
                file.write(full_url + "\n")
                

    file = './urls.txt'
    documents = scrape(file)
    clean_documents(documents)
    save_documents_json(documents, './scraped_data.json')
    
    docs = load_pdf_documents("FAQ") # Load all documents in the directory(success)
    chunks = chunking(docs) # Split documents into chunks
    vectorstore.add_documents(chunks) # Create embeddings and save them in a vector store
    
    page1 = "https://pdx.smartcatalogiq.com/en/2023-2024/bulletin/maseeh-college-of-engineering-and-computer-science/computer-science/"
    page2 = "https://pdx.smartcatalogiq.com/en/2023-2024/bulletin/courses/cs-computer-science/"
    doc = scrape_recursive(page1, 12)
    doc.extend(scrape_recursive(page2, 12))
    save_documents_json(doc, './scraped_data.json')
    scraped_data = load_documents_json('./scraped_data.json')
    chunks = chunking(scraped_data)
    vectorstore.add_documents(chunks)
