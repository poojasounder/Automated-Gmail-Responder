# Replace html2text, it's licensed under GPLv3
# If we use it we have to license entire project under GPL
import html2text 
import json
from bs4 import BeautifulSoup
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.schema import Document
from vertexai.language_models import TextEmbeddingModel, TextGenerationModel
from google.cloud import aiplatform

embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
generation_model = TextGenerationModel.from_pretrained("text-bison@001")

# tweak these for the PSU site
TAGS = ["script", "style", "nav", "footer", "aside", "button", "iframe"]
PATTERN = r"[^\w\s]"
DEPTH = 3
SAVE_FILE = "scraped_data.json"
EMBED_FILE = "embeddings.json"
GCS_DIR = "gs://cs470-rag-llm-embeddings"
INDEX_NAME = "rag-llm-vector-store"
ENDPOINT = "rag-llm-endpoint"
DEPLOYED_ENDPOINT = "rag-llm-endpoint-deployment"
DIMENSIONS = 768 # textembedding-gecko returns 768 dimension embedding vectors


def strip_tags_and_whitespace(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(TAGS):
        tag.decompose()
    return ' '.join(soup.stripped_strings) #stripped_strings removes whitespace

# Removes css and pdf files from Documents list
def remove_extensions(documents):
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
        timeout=500,
        check_response_status=True,
        extractor=strip_tags_and_whitespace
    )
    documents = loader.load()
    documents = remove_extensions(documents)

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


### Functions below this cost money because they call embedding model ###


def text_embedding(text: str):
    embeddings = embedding_model.get_embeddings([text])
    return embeddings[0].values # get_embeddings returns a list

# Takes in Documents list and writes embeddings as JSON file, returns embeddings as list
# Clean this up
def create_embeddings(documents, filename):
    embeddings = []
    embeddings_json = []

    for i, doc in enumerate(documents):
        vector = text_embedding(doc.page_content)
        embeddings.append(vector)
        embeddings_json.append({
            "id": str(i),
            "embedding": vector
        })

    # VertexAI Vector Search Index needs JSONL format, i.e. entries separated by newlines
    with open(filename, 'w+') as f:
        for entry in embeddings_json:
            json.dump(entry, f)
            f.write('\n')
    
    return embeddings


### Something below this is messing up, I'm guessing something to do with index endpoint
#
#def get_context_id(question_vector):
#    index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
#        index_endpoint_name='rag-llm-endpoint-deployment'
#    )
#    if index_endpoint:
#        print(f"Index endpoint resource name: {index_endpoint.name}")
#        print(
#            f"Index endpoint public domain name: {index_endpoint.public_endpoint_domain_name}"
#        )
#        print("Deployed indexes on the index endpoint:")
#        for d in index_endpoint.deployed_indexes:
#            print(f"    {d.id}")
#    result = index_endpoint.find_neighbors(
#        deployed_index_id=ENDPOINT,
#        queries=[question_vector],
#        num_neighbors=5,
#        )
#    print(result)
#
#def get_context_from_documents(documents, result_vector):
#    context = ""
#    for result in result_vector:
#        context += (documents[result].page_content + " ")
#    return context
#
#def text_generation_model(**kwargs):
#    return generation_model.predict(**kwargs).text
#
#def answer_question(question, context):
#    prompt = f""" Answer the question using the provided context. If the answer is
#              not contained in the context, say "answer not available in context" \n\n
#                Context: \n {context} \n
#                Question: \n {question} \n
#                Answer:
#              """
#    return(text_generation_model(prompt=prompt))

if __name__ == "__main__":
    website = "https://www.pdx.edu/computer-science/"
    documents = scrape(website, DEPTH)
    documents = remove_extensions(documents)
    save_documents_json(documents, SAVE_FILE)
    loaded_documents = load_documents_json(SAVE_FILE)
    embeddings = create_embeddings(loaded_documents, EMBED_FILE)
    print(embeddings[0])
#    question = "What cores are in the grad prep program?"
#    question_vector = text_embedding(question)
#    id_vector = get_context_id(question_vector)
#    print(id_vector)
#    context = get_context_from_documents(loaded_documents, id_vector)
#    please_work = answer_question(question, context)

