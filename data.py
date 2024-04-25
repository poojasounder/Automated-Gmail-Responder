import json, os, re, unidecode
from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.schema import Document

SCRAPED_DATA = "documents/scraped_data.json"

def files(path):
    """Returns filenames in given path"""
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def save_documents_json(documents, filename):
    """Saves list of Documents as JSON file"""
    data = [doc.dict() for doc in documents]
    with open(filename, "w+") as f:
        json.dump(data, f)


def load_documents_json(filename):
    """Reads a JSON file and returns a list of Documents"""
    with open(filename, "r") as f:
        data: list = json.load(f)
    return [Document(**doc_dict) for doc_dict in data]


def clean_text(text):
    """Extracts alphanumeric characters and cleans extra whitespace"""
    # Convert Unicode to ASCII
    text = unidecode.unidecode(text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_documents(documents):
    """Cleans page_content text of Documents list"""
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)


def scrape_article(filename):
    """Scrapes URLs listed in file, extracts article tag, returns Documents"""
    # Creates list of URLs
    with open(filename, "r") as file:
        sites = [line.rstrip("\n") for line in file]

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
        use_async=True,
        prevent_outside=True,
        check_response_status=True,
        continue_on_failure=True,
        extractor=extract_text,
    )
    docs = loader.load()
    clean_documents(docs)
    return docs


sites = "urls.txt"
docs = scrape_article(sites)
page1 = "https://pdx.smartcatalogiq.com/en/2023-2024/bulletin/maseeh-college-of-engineering-and-computer-science/computer-science/"
page2 = "https://pdx.smartcatalogiq.com/en/2023-2024/bulletin/courses/cs-computer-science/"
docs.extend(scrape_recursive(page1, 9))
docs.extend(scrape_recursive(page2, 9))
save_documents_json(docs, SCRAPED_DATA)
print("Number of pages:", len(docs))
