# Replace html2text, it's licensed under GPLv3
# If we use it we have to license entire project under GPLv3
import html2text 
import json
import numpy as np
import faiss
from bs4 import BeautifulSoup
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vertexai.language_models import TextEmbeddingModel, TextGenerationModel

embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
generation_model = TextGenerationModel.from_pretrained("text-bison@001")

# tweak these for the PSU site
TAGS = ["script", "style", "nav", "footer", "aside", "button", "iframe"]
PATTERN = r"[^\w\s]"
DEPTH = 3
DOC_FILE = "documents.json"
EMBED_FILE = "embeddings.npy"
FAISS_FILE = "faiss_index"
DIMENSION = 768 # textembedding-gecko returns 768 dimension embedding vectors


def strip_tags_and_whitespace(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(TAGS):
        tag.decompose()
    return ' '.join(soup.stripped_strings) #stripped_strings removes whitespace

# Removes css and pdf files from Documents list
def remove_css_and_pdf(documents):
    extensions_removed = []
    for doc in documents:
        source = doc.metadata["source"]
        # Definitely don't want CSS file but might find a way to use PDF files
        if not source.endswith(".css") or not source.endswith(".pdf"):
                extensions_removed.append(doc)
    return extensions_removed 

# Scrapes given URL and returns list of Document objects
def scrape(url, max_depth):
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=max_depth,
        prevent_outside=True,
        check_response_status=True,
        extractor=strip_tags_and_whitespace
    )
    documents = loader.load()
    documents = remove_css_and_pdf(documents)

    # Replace this with something else
    text_maker = html2text.HTML2Text()
    text_maker.body_width = 0

    for doc in documents:
        doc.page_content = text_maker.handle(doc.page_content)

    return documents

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

if __name__ == "__main__":
#    website = "https://www.pdx.edu/computer-science/"
#    documents = scrape(website, DEPTH)
#    save_documents_json(documents, DOC_FILE)
#    embeddings = create_document_embedding(loaded_documents, EMBED_FILE)
    loaded_documents = load_documents_json(DOC_FILE)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = FAISS.from_documents(loaded_documents, embeddings)
    relevant_docs = db.similarity_search(
        query="What is the University Covid response?",
        k=5,
    )
    print(relevant_docs)