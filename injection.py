from langchain_community.document_loaders import PyPDFDirectoryLoader,AsyncHtmlLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
#from langchain_mistral import Mistral7BEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import PyPDF2
#import PyMuPDF
import os
import shutil
import requests
from pyhtml2pdf import converter
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

def convert_to_pdf(file):

    output_directory = "load_documents"
    os.makedirs(output_directory, exist_ok=True)
    # Read URLs from file
    with open(file, "r") as file:
        urls = file.readlines()
    index = 1
    # Process each URL
    for url in urls:
        
        url = url.strip()  # Remove leading/trailing whitespaces
        if url:  # Skip empty lines
            if url.lower().endswith(".pdf"):
                # Extract filename from URL
                filename = os.path.basename(url)
                # Download the PDF file from the URL
                response = requests.get(url)
                if response.status_code == 200:
                    # Save the PDF file to a temporary location
                    temp_file_path = os.path.join(output_directory, filename)
                    with open(temp_file_path, 'wb') as f:
                        f.write(response.content)
                    # Move the temporary file to the destination directory
                    shutil.move(temp_file_path, os.path.join(output_directory, filename))
                    print(f"PDF file downloaded and uploaded successfully: {filename}")
                else:
                    print(f"Failed to download PDF file from URL: {url}")
            else:
                converter.convert(url, f"./load_documents/doc-{index}.pdf")
                index = index + 1
    return None

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
    
    # Initialize vectorstore
    vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
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
    
    convert_to_pdf('./Upload_documents/urls.txt')
    docs = load_pdf_documents("load_documents") # Load all documents in the directory(success)
    chunks = chunking(docs) # Split documents into chunks(success)
    vectorstore.add_documents(chunks) # Added vectorstore (success)
    #splits = chunking(docs_from_urls) # Split documents into chunks(success)
    #vectorstore.add_documents(documents=splits) # Added vectorstore (success)