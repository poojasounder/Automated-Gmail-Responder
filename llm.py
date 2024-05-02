import re
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.vectorstores import Chroma
#from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAIEmbeddings,ChatOpenAI

"""
try:
    subprocess.run(["python","injection.py"], bufsize=0)
except subprocess.CalledProcessError as e:
    print(f"Error while running the injection.py: {e}")
except Exception as exception:
    print(f"An unexpected error occured: {exception}")
"""

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
def run(llm, prompt, email, docs):
    result = llm.invoke(prompt.format(email=email, context=format_docs(docs)))
    return result

if __name__ == "__main__":
    load_dotenv()

    vectorstore = Chroma(
        embedding_function=OpenAIEmbeddings(),
        persist_directory="./.chromadb"
    )

    llm = ChatOpenAI(model='gpt-3.5-turbo',temperature=0)
    while(1):
        email = input("Ask question: ")
        docs = vectorstore.similarity_search(email)
        rag_prompt = '''
        Task: Write an email response to the following email from a student with answers to their questions given the following context.
        
        Email: {email}
        Context: {context}
        '''
        prompt = PromptTemplate(template=rag_prompt, input_variables=["context", "email"])
        chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)

        response = chain.invoke ({
            "input_documents": docs,
            "email": email
        }, return_only_outputs=True)
        print('\n'+response["output_text"]+'\n')


