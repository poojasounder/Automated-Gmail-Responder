from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain.prompts import PromptTemplate

'''Defining the models specifically the llm model for text and embedding model'''
llm = VertexAI(
    model_name="text-bison@001",
    max_output_tokens=512,
    temperature=0.1,
    top_p=0.8,
    top_k=40,
    verbose=True,
)

EMBEDDING_QPM = 15
EMBEDDING_NUM_BATCH = 2
embeddings = VertexAIEmbeddings(
    project_id="cs470-rag-llm",
    location="us-central1",
    qpm=EMBEDDING_QPM,
    num_batch=EMBEDDING_NUM_BATCH,
)

''' Testing out the llm for text model '''
my_text = "Which is the parent company of Lincoln"

print(llm.invoke(my_text))

text = "Alphabet is the parent company of Google"

''' Testing out the embedding model '''
text_embedding = embeddings.embed_query(text)

print(f"Your embedding is length {len(text_embedding)}")
print(f"Here's a sample: {text_embedding[:5]}...")

'''Prompts are text used as instructions to your model'''
prompt = """
Meta is the parent company of Twitter.

What is wrong with that statement?
"""

print(llm.invoke(prompt))

''' Prompt Template is an object that helps to create prompts based on a combination of user input'''

template = """
I really want to travel to {location}. What should I do there?

Respond in one short sentence
"""

prompt = PromptTemplate(
    input_variables=["location"],
    template=template,
)

final_prompt = prompt.format(location="Mumbai")

print(f"Final Prompt: {final_prompt}")
print(".........")
print(f"LLM Output: {llm.invoke(final_prompt)}")

