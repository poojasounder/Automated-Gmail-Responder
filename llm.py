from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

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
    llm = GoogleGenerativeAI(model="gemini-pro")
    # to use the vectorstore
    retriever = vectorstore.as_retriever()
    email = "Hi Ella, my name is Julie Nguyen and I am interested in the Graduate program. I have a few questions about the program. Can you tell me more about the courses offered in the program? Also, I would like to know about the admission requirements and the application process. Thank you."
    docs = vectorstore.similarity_search(email,k=3) # Get relevant documents based on the query(success)
    rag_prompt = '''
    Your name is Ella and you are a CS graduate advisor at Portland State University. 
    Your job is to respond to student's emails regarding questions about CS graduate programs at Portland State. 
    Given the following email: {email}, write a response to the student in the format similar to below with answers to their questions based on the given
    context: {context}
    Answer like a human in a professional matter, professional vocabulary,
      and do not include any special characters except bullet points.
    For example:
    Email: Hi Ella, I do have a few questions. What are the admission requirements? Thanks,Pooja
    Response:
    Thanks for reaching out. I am happy to provide you with the answers to your questions.
    The admission requirements for our CS graduate program are:
    1. A bachelor's degree in computer science or a related field from an accredited university.
    2. A GPA of 3.0 or higher.
    3. GRE scores of at least 150 verbal and 150 quantitative.
    4. A personal statement.

    Here are some more rules:
    If someone doesn't ask or say anything regarding computer science, simply answer with 
    "I'm sorry, I am unable to answer your question. I can only answer any questions regarding
    the Master of Science Program, but feel free to ask me any other questions!".
    If someone did not ask any question or any statement that is not relevant to the program
    or computer science program, just reply with "Hi there, I am unsure of what you are asking. Could
    you ask me again in more detail? Thank you.".
    If someone asks for anything regarding the name of the courses, provide the course name
    as well as the CS course number. Something like "CS100 - Intro to CS". So if you provide
    any course information to the student's, make sure you include the name of the course as wel
    as its course number, such as "CS100 - Intro top CS". 
    Ensure that the format of your output is not all clunked up together. Remember, your response
    will be emailed back to the student, so we don't want the email to be all cluttered, ensure
    proper formatting with spaces, indents, and newlines when necessary. 
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
    yes = 1
    while(yes):
        email = input("Question: ")
        print("\n")
        result = rag_chain.invoke(email)
        print(result)