#from langchain_openai import ChatOpenAI
import time
from dotenv import load_dotenv
#from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
#from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import (
    GoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()
loader = WebBaseLoader("https://www.pdx.edu/computer-science/master")
llm = GoogleGenerativeAI(model="gemini-pro")
output_parser = StrOutputParser()
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
# embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query")
chromadb = Chroma.from_documents(documents, embedding_function) #chroma use
retriever = chromadb.as_retriever()

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)
retriver_chain = create_retrieval_chain(retriever, document_chain)
#chain = prompt | llm | output_parser
#result = chain.invoke({"input": "how can langsmith help with testing"})

def TypeOutResponse(response: str):
    for char in response:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()
#print(result)
while True:
    q: str = input("Enter q: ")
    result = retriver_chain.invoke({"input": q})
    #print(result["answer"])
    TypeOutResponse(response=result["answer"])


