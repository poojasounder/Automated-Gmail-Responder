import os
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

from langsmith import traceable, Client

load_dotenv()

LANGCHAIN_API_KEY = os.environ["LANGCHAIN_API_KEY"]


@traceable
def init_vectorstore():
    vectorstore = Chroma(
        embedding_function=GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", task_type="retrieval_query"
        ),
        persist_directory="./.chromadb",
    )
    return vectorstore


@traceable
def init_llm():
    llm = GoogleGenerativeAI(model="gemini-pro")
    return llm


@traceable
def search_vectorstore(vectorstore, email):
    docs = vectorstore.similarity_search(
        email
    )  # Get relevant documents based on the query(success)
    return docs


@traceable
def init_prompt():
    rag_prompt = """
    Your role: You are a CS Graduate Advisor at Portland State University
    Your Job: Your job is to respond to emails from students regarding any questions about CS graduate programs
    Task: Write an email response to the following email from a student with answers to their questions given the following context.

    Email: {email}
    Context: {context}

    If you need more information, please ask for it or if you don't have the context,
    you can write an email response saying "Sorry,I am not able to find the provide the answers to your questions"
    Include all relevant infomation in your response.
    """

    prompt = PromptTemplate(template=rag_prompt, input_variables=["context", "email"])
    return prompt


@traceable
def generate_response(llm, prompt, email, docs):
    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    response = chain.invoke(
        {"input_documents": docs, "email": email}, return_only_outputs=True
    )
    return response


@traceable
def full_process(email):
    vectorstore = Chroma(
        embedding_function=GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", task_type="retrieval_query"
        ),
        persist_directory="./.chromadb",
    )

    llm = GoogleGenerativeAI(model="gemini-pro")

    docs = vectorstore.similarity_search(
        email
    )  # Get relevant documents based on the query(success)

    rag_prompt = """
    Your role: You are a CS Graduate Advisor at Portland State University
    Your Job: Your job is to respond to emails from students regarding any questions about CS graduate programs
    Task: Write an email response to the following email from a student with answers to their questions given the following context.

    Email: {email}
    Context: {context}

    If you need more information, please ask for it or if you don't have the context,
    you can write an email response saying "Sorry,I am not able to find the provide the answers to your questions"
    Include all relevant infomation in your response.
    """

    prompt = PromptTemplate(template=rag_prompt, input_variables=["context", "email"])

    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    response = chain.invoke(
        {"input_documents": docs, "email": email}, return_only_outputs=True
    )
    return response


if __name__ == "__main__":
    email = "What classes do I have to take to complete the Master's program?"
    client = Client()
    # response = full_process(email)
    # print(response)

    vectorstore = init_vectorstore()
    llm = init_llm()
    docs = search_vectorstore(vectorstore, llm)
    prompt = init_prompt()
    generate_response(llm, prompt, email, docs)
