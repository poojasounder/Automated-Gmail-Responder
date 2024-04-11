from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# format the documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# run the llm
def run(llm,prompt,email,docs):
    result = llm.invoke(prompt.format(email=email,context=format_docs(docs)))
    return result

if __name__ == "__main__":
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
    email = """Hi Ella,
                I do have a few questions.
                What are the admission requirements?
                Thanks,Pooja"""
    docs = retriever.get_relevant_documents(email) # Get relevant documents based on the query(success)
    
    rag_prompt = '''
    Your name is Ella and you are a CS graduate advisor at Portland State University. 
    Your job is to respond to student's emails regarding questions about CS graduate programs at Portland State. 
    Given the following email: {email}, write a response email to the student in the format similar to below with answers to their questions based on the given
    context: {context}
    Answer like a human and do not include any special characters except bullet points.
    For example:
    Email: Hi Ella, I do have a few questions. What are the admission requirements? Thanks,Pooja
    Response: 
    Hi Pooja,
    Thanks for reaching out. I am happy to provide you with the answers to your questions.
    The admission requirements for our CS graduate program are:
    1. A bachelor's degree in computer science or a related field from an accredited university.
    2. A GPA of 3.0 or higher.
    3. GRE scores of at least 150 verbal and 150 quantitative.
    4. A personal statement.
    Best Regards,
    Ella
    CS graduate advisor
    Portland State University
    '''
    prompt = PromptTemplate(
        input_variables=["email", "context"],
        template=rag_prompt
    )
    
    # invoke the llm model
    result = run(llm,prompt,email,docs) # invoke the model(success)
    print(result) # might delete later when integrating with frontend