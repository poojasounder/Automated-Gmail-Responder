import vertexai
#from vertexai_community.preview.generative_models import GenerativeModel, ChatSession
from langchain_google_vertexai import VertexAI  # type: ignore
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


# TODO(developer): Update and un-comment below lines
project_id = "cs470-rag-llm"
location = "us-central1"
vertexai.init(project=project_id, location=location)

#model = VertexAI(model_name="gemini-pro")

#message = "What are some of the pros and cons of Python as a programming language?"
#model.invoke(message)

#print(model.invoke(message))

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

#doc1 = PyPDFLoader(r"C:\Users\15042\Automated-Gmail-Responder\documents\2023-2024 Bulletin.pdf")
#pages1 = doc1.split_text(doc1)
#faiss_index = FAISS.from_documents(pages1, OpenAIEmbeddings())

doc2 = PyPDFLoader(r"C:\Users\15042\Automated-Gmail-Responder\documents\CS Graduate Admissions - Frequently Asked Questions (FAQ).pdf")
pages2 = doc2.load_and_split()
faiss_index = FAISS.from_documents(pages2, OpenAIEmbeddings())

docs = faiss_index.similarity_search("How many credits do I need for upper-division?", k=2)
for doc in docs:
    print(str(doc.metadata["page"]) + ":", doc.page_content[:300])

''' chat = model.start_chat()

def get_chat_response(chat: ChatSession, prompt: str):
    response = chat.send_message(prompt)
    return response.text

prompt = "Hello."
print(get_chat_response(chat, prompt))

prompt = "What are all the colors in a rainbow?"
print(get_chat_response(chat, prompt))

prompt = "Why does it appear when it rains?"
print(get_chat_response(chat, prompt)) '''