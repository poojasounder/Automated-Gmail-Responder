import os
# import vertexai

# from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader
# from langchain_community.llms import VertexAI
# from langchain_google_vertexai import VertexAIEmbeddings
# from langchain.retrievers import GoogleVertexAISearchRetriever
# from langchain.chains import ConversationalRetrievalChain
# from langchain.memory import ConversationBufferMemory
# from langchain_community.retrievers import GoogleVertexAIMultiTurnSearchRetriever
# from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import GCSFileLoader
from langchain.text_splitter import CharacterTextSplitter
# from langchain_google_vertexai import VertexAIEmbeddings
from vertexai.language_models import TextEmbeddingModel

from dotenv import load_dotenv

# -- Load environment variables -- #
load_dotenv()
DATA_STORE_ID = os.environ['DATA_STORE_ID']
PROJECT_ID = os.environ['PROJECT_ID']
DATA_STORE_LOCATION = os.environ['DATA_STORE_LOCATION']
REGION = os.environ['REGION']
MODEL = os.environ["MODEL"]
BUCKET_NAME = os.environ['BUCKET_NAME']

# -- Load Google Bucket Documents -- #
'''
print("LOADING BUCKET DOCUMENTS...")

bucket_name = '2023-2024 Bulletin.pdf' #'CS Graduate Admissions - Frequently Asked Questions (FAQ).pdf']
def load_google_bucket_documents(bucket_name: str) -> str:
  bucket_loader = GCSFileLoader(project_name=PROJECT_ID, bucket=BUCKET_NAME, blob=bucket_name)
  return bucket_loader.load()[0].page_content

bucket_doc = load_google_bucket_documents(bucket_name)
with open("bucket_content.txt", "w") as f:
  f.write(bucket_doc)

print("BUCKET DOCUMENTS LOADED")
'''

print("LOADING BUCKET DOCUMENTS COMPLETED")

# -- Chunking Documents -- #
print("CHUNKING DOCUMENTS...")

def chunk_docs(bucket_content: str) -> list[str]:
  text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function = len
  )
  chunked_docs = text_splitter.split_text(bucket_content)
  return chunked_docs

with open("bucket_content.txt", "r") as f:
  bucket_content = f.read()

chunked_docs = chunk_docs(bucket_content)
print("CHUNKING DOCUMENTS COMPLETED")


# -- Embed Chunks -- #
print("EMBEDDING CHUNKS...")



def text_embedding(chunked_docs: str) -> list:
    """Text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([chunked_docs])
    for embedding in embeddings:
        vector = embedding.values
        print(f"Length of Embedding Vector: {len(vector)}")
    return vector


print(text_embedding(chunked_docs[0]))
print("EMBEDDING CHUNKS COMPLETED")



# doc_result = embeddings.embed_documents([text])  

'''
# -- Load Local Documents -- #
DOC_DIR = 'documents/'

def get_documents(doc_dir):
  docs = {}
  for filename in os.listdir(doc_dir):
    doc_type = filename.split('.')[-1]
    match doc_type:
      case 'pdf':
        docs[filename] = PyPDFLoader(os.path.join(DOC_DIR, filename)).load_and_split()
      case 'html':
        docs[filename] = UnstructuredHTMLLoader(os.path.join(DOC_DIR, filename)).load()
      case 'txt':
        docs[filename] = open(os.path.join(DOC_DIR, filename)).read()
      case _:
        print('unable to load: unknown doc type')
        continue
  return docs

docs = get_documents(DOC_DIR)

# -- Generate embeddings -- #
embeddings = VertexAIEmbeddings()
# query_result = embeddings.embed_query(text)embeddings = VertexAIEmbeddings()
# doc_result = embeddings.embed_documents([text])


# -- Vertex AI Initialization -- #
vertexai.init(project=PROJECT_ID, location=REGION)
llm = VertexAI(model_name=MODEL)


# -- Base Retriever -- #
retriever = GoogleVertexAISearchRetriever(
    project_id=PROJECT_ID,
    location_id=DATA_STORE_LOCATION,
    data_store_id=DATA_STORE_ID,
    get_extractive_answers=True,
    max_documents=10,
    max_extractive_segment_count=1,
    max_extractive_answer_count=5,
)


# -- Conversational Retriever -- #
multi_turn_retriever = GoogleVertexAIMultiTurnSearchRetriever(
    project_id=PROJECT_ID, location_id=DATA_STORE_LOCATION, data_store_id=DATA_STORE_ID
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversational_retrieval = ConversationalRetrievalChain.from_llm(
    llm=llm, retriever=multi_turn_retriever, memory=memory
)


# -- Prompt Engineering -- #
prompt_template = """Use the context to answer the question at the end.
You must always use the context and context only to answer the question. Never try to make up an answer. If the context is empty or you do not know the answer, just say "I don't know".
The answer should consist of only 1 word and not a sentence.

Context: {context}

Question: {question}
Helpful Answer:
"""
prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm, prompt=prompt, retriever=retriever, return_source_documents=True
)


question = "What were alphabet revenues in 2022?"

result = conversational_retrieval({"question": question})
print(result["answer"])
'''