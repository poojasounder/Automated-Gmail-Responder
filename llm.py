import re
import subprocess
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

'''
try:
    subprocess.run(["python","injection.py"], bufsize=0)
except subprocess.CalledProcessError as e:
    print(f"Error while running the injection.py: {e}")
except Exception as exception:
    print(f"An unexpected error occured: {exception}")
'''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# format the documents
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# run the llm
def run(llm,prompt,email,docs):
    result = llm.invoke(prompt.format(email=email,context=format_docs(docs)))
    return result

@app.get("/")
def aerllm(q:Union[str,None] = None):
    email: str = None
    # loading environment variables
    load_dotenv()

    #grabbing the embeddings
    vectorstore = Chroma(
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
        persist_directory="./.chromadb"
    )
    #initialized the llm model
    llm = GoogleGenerativeAI(model="gemini-pro")
    # to use the vectorstore
    retriever = vectorstore.as_retriever()
    if q is not None:
        email = q
    else:
        raise ValueError("No valid question given")
    docs = vectorstore.similarity_search(email,k=3) # Get relevant documents based on the query(success)
    rag_prompt = '''
    Your role: You are a CS Graduate Advisor at Portland State University
    Your Job: Your job is to respond to emails from students regarding any questions about CS graduate programs
    Task: Write an email response to the following email from a student with answers to their questions given the following context.

    Email: {email}
    Context: {context}

    If you need more information, please ask for it or if you don't have the context,
    you can write an email response saying "Sorry,I am not able to find the provide the answers to your questions"
    If the questions are not related to computer science major, write an email response directing the student to the appropriate department.
    '''
    prompt = PromptTemplate.from_template(rag_prompt)
    # invoke the llm model
    #result = run(llm, prompt, email, docs)
    #print(result) # might delete later when integrating with frontend
    """ qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    ) """

    rag_chain = (
        {"context": retriever | format_docs, "email": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    result = rag_chain.invoke(email)
    result = re.sub(r"\n", "<div><br></div>", result)
    return {"response": result}
