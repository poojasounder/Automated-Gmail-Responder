from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langsmith import traceable, Client

load_dotenv()

@traceable
def init_vectorstore():
    '''Initializes vectorstore'''
    return Chroma(
        embedding_function=OpenAIEmbeddings(),
        persist_directory="./.chromadb",
    )


@traceable
def init_llm():
    '''Initializes llm'''
    return ChatOpenAI(model='gpt-3.5-turbo',temperature=0)


@traceable
def search_vectorstore(vectorstore, email: str):
    '''Performs search on vectorstore and returns relevant documents'''
    return vectorstore.similarity_search(email)


@traceable
def init_prompt():
    '''Initializes system prompt'''
    rag_prompt = '''
    Task: Write an email response to the following email from a student with answers to their questions given the following context.
    
    Email: {email}
    Context: {context}
    '''
    return PromptTemplate(template=rag_prompt, input_variables=["context", "email"])


@traceable
def generate_response(llm, prompt, email, docs):
    '''Generates a response for email, given prompt and relevant documents'''
    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    response = chain.invoke(
        {"input_documents": docs, "email": email}, return_only_outputs=True
    )
    return response


if __name__ == "__main__":
    # modify the email variable to test different responses
    email = "What classes do I have to take to complete the Master's program?"
    client = Client()

    vectorstore = init_vectorstore()
    llm = init_llm()
    docs = search_vectorstore(vectorstore, email)
    prompt = init_prompt()
    response = generate_response(llm, prompt, email, docs)
    print(response)
