from urllib.parse import urljoin
from langchain_community.document_loaders import PyPDFDirectoryLoader, AsyncChromiumLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import PyPDF2
import os, re, json
import requests
from pyhtml2pdf import converter
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
    # Extract article tag
    transformer = BeautifulSoupTransformer()
    docs_tr = transformer.transform_documents(
        documents=docs,
        tags_to_extract=['article']
    )

    return docs_tr

# combine what's in the data.py on branch data to clean up the docs and chunking process.
def find_page_numbers(input_pdf_path, start_keyword, end_keyword):
    start_page = None
    end_page = None

    with open(input_pdf_path, "rb") as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)

        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            text = page.extract_text()

            if start_keyword in text and start_page is None:
                start_page = page_number + 1  # Adjust to 1-based indexing
            elif end_keyword in text:
                end_page = page_number + 1  # Adjust to 1-based indexing
                break

    return start_page, end_page
def extract_and_save_pages(input_pdf_path, output_pdf_path, start_page, end_page):
    with open(input_pdf_path, "rb") as input_file, open(output_pdf_path, "wb") as output_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_number in range(start_page - 1, end_page):  # Adjust to 0-based indexing
            pdf_writer.add_page(pdf_reader.pages[page_number])

        pdf_writer.write(output_file)

def load_pdf_documents(dir):
    loader = PyPDFDirectoryLoader(dir)
    docs = loader.load()
    return docs

def chunking(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=2000)
    chunks = text_splitter.split_documents(documents)
    return chunks

if __name__ == "__main__":
    # loading environment variables
    load_dotenv()
    
    # Gets all the relevent URL's from the CS department and adds it to url.txt file
    response = requests.get("https://www.pdx.edu/computer-science/")
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    # Open a file in write mode
    with open("./Upload_documents/urls.txt", "w") as file:
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'computer-science' in href:
                full_url = urljoin("https://www.pdx.edu/computer-science/", href)
                file.write(full_url + "\n")
                
    # Initialize vectorstore
    vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large", dimensions=768),
    persist_directory="./.chromadb"
    )
    
    # Provide the path to your input PDF file
    input_pdf_path = "./Upload_documents/Bulletin.pdf"
    # Find the start and end page numbers
    start_page, end_page = find_page_numbers(input_pdf_path, "COMPUTER SCIENCE M.S.", "Electrical and Computer Engineering")

    # Provide the path for the output PDF file
    output_pdf_path = "./load_documents/bulletin_cs.pdf"

    # Extract and save the specified pages as a new PDF file
    if start_page is not None and end_page is not None:
        extract_and_save_pages(input_pdf_path, output_pdf_path, start_page, end_page)
        
    start_page, end_page = find_page_numbers(input_pdf_path,"Portland State University", "UNDERGRADUATE STUDIES")
    # Provide the path for the output PDF file
    output_pdf_path = "./load_documents/Finance.pdf"

    # Extract and save the specified pages as a new PDF file
    if start_page is not None and end_page is not None:
        extract_and_save_pages(input_pdf_path, output_pdf_path, start_page, end_page)
        
    file = './Upload_documents/urls.txt'
    documents = scrape(file)
    clean_documents(documents)
    save_documents_json(documents, './scraped_data.json')
    scraped_data = load_documents_json('./scraped_data.json')
    chunks = chunking(scraped_data)
    vectorstore.add_documents(chunks)
    
    #convert_to_pdf('./Upload_documents/urls.txt')
    docs = load_pdf_documents("load_documents") # Load all documents in the directory(success)
    chunks = chunking(docs) # Split documents into chunks(success)
    vectorstore.add_documents(chunks) # Added vectorstore (success)
    #splits = chunking(docs_from_urls) # Split documents into chunks(success)
    #vectorstore.add_documents(documents=splits) # Added vectorstore (success)