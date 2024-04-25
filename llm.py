from langchain_community.vectorstores import Chroma
#from langchain_mistral import Mistral7B, Mistral7BEmbeddings
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain

# format the documents
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

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
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
    # to use the vectorstore
    retriever = vectorstore.as_retriever()
    email = "Hi, What are the courses required to graduate from the  CS masters program?"
    #my name is Julie Nguyen and I am interested in the Graduate program. I wanted to know what the requirements are to be admitted into the program. I have a 2.9 GPA and 1 year experience from my internship at Intel. I want to learn more about Computer Science and thrive with my future career in game development. Thank you! Best regards, Julie Nguyen"
    docs = vectorstore.similarity_search(email,k=3) # Get relevant documents based on the query(success)
    rag_prompt = '''
    Your role: You are a CS Graduate Advisor at Portland State University
    Your Job: Your job is to respond to emails from students regarding any questions about CS graduate programs and keep the email response as short as possible
    Task: Write an email response to the following email from a student with answers to their questions given the following context.
    
    Email: {email}
    Context: {context}
    
    If you need more information, please ask for it or if you don't have the context,
    you can write an email response saying "Sorry,I am not able to find the provide the answers to your questions"
    Ignore unrelated information in the context
    '''
    prompt = PromptTemplate.from_template(rag_prompt)

    qa_chain = create_stuff_documents_chain(llm, prompt)
    result = qa_chain.invoke({"context": docs, "email": email})
    print(result)