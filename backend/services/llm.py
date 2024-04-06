import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.prompts import PromptTemplate

from services.database import create_vector_store, load_vector_store, update_vector_store 
from services.data_processing import url_to_pdf, chunk_pdf

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
DATABASE_URI = os.getenv("DATABASE_URI")

# LLM configuration
llm = GoogleGenerativeAI(model="gemini-pro")
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

# prompt
prompt_template = """Give the response for the following question:{question} given the following {context}"""
qna_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=prompt_template
)

def answer_question(question, prompt=qna_prompt):
    '''Getting an answer to a question given the prompt'''
    # TODO: find a solution so that we don't have to load the vector store
    # everytime we ask a question

    # attempt to load the vector store
    try:
        vector_store = load_vector_store(embeddings)
    except:
        print("Could not find vector store.")
        return

    # retrieve the relevant documents
    retriever = vector_store.as_retriever()
    context = retriever.get_relevant_documents(question)

    # get answer from the llm
    return {"answer": llm.invoke(prompt.format(question=question, context=context))}

def add_embeddings(document):
    '''Adds document as embeddings to a vector store'''
    match document.doc_type:
        case "URL":
            pdf = url_to_pdf(document.value)
            chunks = chunk_pdf(pdf)
        case "PDF":
            chunks = chunk_pdf(document.value)
        case _:
            print("Unknown document type")

    # if our local database already exists, update it
    if os.path.exists(os.path.join(os.getcwd(), DATABASE_URI)):
        update_vector_store(chunks, embeddings)
    # else create a new faiss database
    else:
        create_vector_store(chunks, embeddings)
    return True
