from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv


if __name__ == "__main__":
    # loading environment variables
    load_dotenv()
    
    vectorstore = Chroma(
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
        persist_directory="./.chromadb"
    )
    
    retriever = vectorstore.as_retriever()
    query = "What are the admission documents?"
    docs = retriever.get_relevant_documents()
    
    rag_prompt = '''Your name is Ella and you are a CS graduate advisor at Portland State University. Your job is to respond
    to student's emails regarding questions about CS graduate programs at Portland State. Given the following email: {email}, write a 
    response email to the student with answers to their questions based on the given context: {context}
    '''
    
    llm = GoogleGenerativeAI(model="gemini-pro")