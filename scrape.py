import json
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader

# Definitely don't want CSS file but might find a way to use PDF files
REMOVE_SITES = [".css", ".pdf"]
SCRAPED_DATA = "documents/scraped_data.json"
MAX_DEPTH = 4

# Saves list of Documents as JSON file
def save_documents_json(documents, filename):
    data = [doc.dict() for doc in documents]
    with open(filename, 'w+') as f:
        json.dump(data, f)

# Reads a JSON file and returns a list of Documents
def load_documents_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return [Document(**doc_dict) for doc_dict in data]

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    # First checks for an article tag
    article_tag = soup.find("article")
    if article_tag:
        return article_tag.get_text(' ', strip=True)
    # If no article tag, check for div tag with matching id
    div_contents = soup.find("div", id="contents")
    if div_contents:
         return div_contents.get_text(' ', strip=True)
    # Returns all text on page
    return ' '.join(soup.stripped_strings)

# Removes css and pdf files from Documents list
def remove_css_and_pdf(documents):
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

# Scrapes given URL and returns list of Document objects
def scrape(url, max_depth):
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