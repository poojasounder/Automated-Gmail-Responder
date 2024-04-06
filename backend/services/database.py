import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")

def create_vector_store(chunks: list[str], embedding):
    '''Creates a vector store from a list of chunks'''
    # TODO: create a vector store on the cloud
    vector_store = FAISS.from_texts(chunks, embedding=embedding)

    # for now we save vector store locally
    vector_store.save_local(DATABASE_URI)
    return vector_store

def load_vector_store(embeddings):
    '''Loads a vector store from local filesystem'''
    if not os.path.exists(os.path.join(os.getcwd(), DATABASE_URI)):
        raise FileNotFoundError(f"Could not find vector store")

    vector_store = FAISS.load_local(
        folder_path=DATABASE_URI, 
        embeddings=embeddings, 
        allow_dangerous_deserialization=True)
    return vector_store

def update_vector_store(chunks: list[str], embeddings):
    '''Updating vector store with new chunks'''
    # TODO: find a more elegant solution to updating the vector store
    # at the moment we are just creating a new vector store and merging them together
    new_vector_store = create_vector_store(chunks, embeddings)
    old_vector_store = load_vector_store(embeddings)
    updated_vector_store = old_vector_store.merge_from(new_vector_store)
    return updated_vector_store