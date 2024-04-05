from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


loader = PyPDFLoader('FAQ.pdf')
pages = loader.load_and_split()


#text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=1000)
#chunks = text_splitter.split_text(pages)


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = Chroma.from_documents(pages,embedding=embeddings)
print(vector_store)
#vector_store.save_local("faiss_index")
#results = vector_store.similarity_search("What are the admission requirements?")
#print(results)
#retriever = vector_store.as_retriever()
#question = "How is the weather today?"
#relevant_docs = retriever.get_relevant_documents(question)
#print(relevant_docs)
#question_blob = storage.Blob.from_string(question)
#question_embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001").embed_query(question_blob)
#relevant_vectors = vector_store.similarity_search(question_embedding)
#print(relevant_vectors)
