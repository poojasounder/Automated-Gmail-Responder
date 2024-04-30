import json
import os
import re
import unidecode
from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.schema import Document

SCRAPED_DATA = "documents/scraped_data.json"


def files(path: str):
    """Returns filenames in given path"""
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def list_from_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        lines = [line.rstrip("\n") for line in file]
    return lines


def save_documents_json(documents: list[Document], filename: str):
    """Saves list of Documents as JSON file"""
    data = [doc.dict() for doc in documents]
    with open(filename, "w+") as file:
        json.dump(data, file)


def load_documents_json(filename: str) -> list[Document]:
    """Reads a JSON file and returns a list of Documents"""
    with open(filename, "r") as file:
        data: list = json.load(file)
    return [Document(**doc_dict) for doc_dict in data]


def clean_text(text: str) -> str:
    """Converts unicode characters and removes extra whitespace

    Args:
        text : The string to be cleaned

    Returns:
        The cleaned string
    """
    text = unidecode.unidecode(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_documents(documents: list[Document]):
    """Runs clean_text on page_content of Documents

    Args:
        documents: List of Documents to be cleaned
    """
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)


def scrape_article(filename: str) -> list[Document]:
    """Scrapes URLs listed in file and extracts article tag

    Args:
        filename: Text file with URLs listed on separate lines

    Returns:
        The contents of the web pages as Documents
    """
    sites = list_from_file(filename)
    # Scrapes list of sites
    loader = AsyncChromiumLoader(sites)
    loader.requests_kwargs = {"verify": False}
    docs = loader.load()
    # Extract article tag
    transformer = BeautifulSoupTransformer()
    docs_transformed = transformer.transform_documents(
        documents=docs, tags_to_extract=["article"]
    )
    clean_documents(docs_transformed)
    return docs_transformed


def extract_text(html: str) -> str:
    """Function used by loader to extract text from div tag with matching id

    Args:
        html: Raw html

    Returns:
        Extracted text as string
    """
    soup = BeautifulSoup(html, "html.parser")
    div_main = soup.find("div", {"id": "main"})
    if div_main:
        return div_main.get_text(" ", strip=True)
    return " ".join(soup.stripped_strings)


def scrape_recursive(url: str, depth: int = 12) -> list[Document]:
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


pdx_sites = "urls.txt"
docs = scrape_article(pdx_sites)
bulletin_sites = list_from_file("bulletin_urls.txt")
for site in bulletin_sites:
    docs.extend(scrape_recursive(site))
save_documents_json(docs, SCRAPED_DATA)
print("Number of pages:", len(docs))
