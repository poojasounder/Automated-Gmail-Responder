import pprint
from ingest import *
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

#website = "https://www.pdx.edu/computer-science/"
#scrape(website, MAX_DEPTH)

scraped_data = load_documents_json(SCRAPED_DATA)
pprint.pprint(scraped_data)
print("Number of pages scraped:", len(scraped_data))

pages = scraped_data[:10]
doc = Document(**json.loads("""
{"page_content": "Coronavirus Response Due to concerns related to the spread of COVID-19, the Department of Computer Science is currently operating during regular hours but relying on virtual meetings, except for absolutely critical activities. Please contact an appropriate person on the list below if you need help via email or if you would like to arrange a time for a phone call or an in-person or online meeting. Undergraduate Advising: uccs@pdx.edu Graduate Advising: gccs@pdx.edu Department Manager: sarreal@pdx.edu Department Chair: mpj@pdx.edu CS Office: csoffice@pdx.edu Please visit https://www.pdx.edu/coronavirus-response for additional information, resources, and updates. CS Tutors (Undergraduate Lower Division Courses) We have transitioned CS Tutoring to an online format using slack as our primary form of contact. \u00a0(If you have not previously used slack: please visit pdx-cs.slack.com , click the \u201ccreate an account\u201d link and follow the instructions on screen. Once you are logged in, click on the \u201ccshelp\u201d channel in the sidebar on the left.) Tutors will be available on Monday to Friday (11am-6pm) and on Saturday (12-6pm). Their primary role is to provide help for CS 161, CS 162, \u00a0CS 163, and CS 202. The tutors may also be able to provide some support for CS 201, CS 250, and CS 251. For the latter group of courses, however, it is recommended (and for all other courses not listed here, it is required) that students contact their instructor or class TA for help. A student can request help from a tutor by posting a short message on the cshelp slack channel that includes the class number and a very brief description of the problem that they need help with. These messages are public so they must not include any personal details, including code or any other part of a student\u2019s solution to a problem. A tutor will then follow-up using direct messaging and, if appropriate, may also offer a zoom meeting for one-on-one interaction. If the tutor determines that a given question can be answered without personal information, and that the answer may be useful to other students, then they may respond by starting a new public thread instead. All conversations with a tutor must begin with a posting on the cshelp channel; it is important that students do not otherwise direct message tutors with questions.", "metadata": {"source": "https://www.pdx.edu/computer-science/coronavirus-response", "title": "Coronavirus Response | Portland State University", "language": "en"}, "type": "Document"}
                 """))
pages.append(doc)

# db = FAISS.from_documents(documents=scraped_data, embedding=embeddings)
db = FAISS.from_documents(documents=pages, embedding=embeddings)
docs = db.similarity_search(query="What is the university Coronavirus response?",k=3)
pprint.pprint(docs)

#create_faiss()
#print("FAISS created")
#
#vector_store = FAISS.load_local(INDEX, embeddings, allow_dangerous_deserialization=True)
#print("FAISS loaded")
# 
#retriever = vector_store.as_retriever()
#llm = GoogleGenerativeAI(model="gemini-pro")
#
#prompt_template = """Give the response for the following question:{question} given the following {context}"""
#
## create a prompt example from above template
#spam_detect_prompt = PromptTemplate(
#    input_variables=["question", "context"],
#    template=prompt_template
#)
#
#while True:
#    line = input("Question>> ")
#    if line:
#        result = llm.invoke(spam_detect_prompt.format(question=line, context=retriever.get_relevant_documents(line)))
#        print(result)
#    else:
#        break
#