# Derived from https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/use-cases/document-qa/question_answering_documents_langchain_matching_engine.ipynb
import glob
import os
import re
import warnings
import numpy as np
import pandas as pd
import textract
from PyPDF2 import PdfReader
from tenacity import retry, stop_after_attempt, wait_random_exponential
from vertexai.language_models import TextEmbeddingModel, TextGenerationModel

warnings.filterwarnings("ignore")

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(10))
def text_generation_model_with_backoff(**kwargs):
    return generation_model.predict(**kwargs).text


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(10))
def embedding_model_with_backoff(text=[]):
    embeddings = embedding_model.get_embeddings(text)
    return [each.values for each in embeddings][0]

def create_data_packet(file_name, file_type, page_number, file_content):
    """Creating a simple dictionary to store all information (content and metadata)
    extracted from the document"""
    data_packet = {}
    data_packet["file_name"] = file_name
    data_packet["file_type"] = file_type
    data_packet["page_number"] = page_number
    data_packet["content"] = file_content
    return data_packet

def files(path):
    """
    Function that returns only filenames (and not folder names)
    """
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

# The function get_chunks_iter() can be used to split a piece of text into smaller chunks,
# each of which is at most maxlength characters long.
# This can be useful for tasks such as summarization, question answering, and translation.
def get_chunks_iter(text, maxlength):
    """
    Get chunks of text, each of which is at most maxlength characters long.

    Args:
        text: The text to be chunked.
        maxlength: The maximum length of each chunk.

    Returns:
        An iterator over the chunks of text.
    """
    start = 0
    end = 0
    final_chunk = []
    while start + maxlength < len(text) and end != -1:
        end = text.rfind(" ", start, start + maxlength + 1)
        final_chunk.append(text[start:end])
        start = end + 1
    final_chunk.append(text[start:])
    return final_chunk


# function to apply "get_chunks_iter" function on each row of dataframe.
# currently each row here for file_type=pdf is content of each page and for other file_type its the whole document.
def split_text(row):
    chunk_iter = get_chunks_iter(row, 5000)
    return chunk_iter

def get_dot_product(row):
    return np.dot(row, query_vector)

def get_context_from_question(question, vector_store, sort_index_value=2):
    global query_vector
    query_vector = np.array(embedding_model_with_backoff([question]))
    top_matched = (
        vector_store["embedding"]
        .apply(get_dot_product)
        .sort_values(ascending=False)[:sort_index_value]
        .index
    )
    top_matched_df = vector_store[vector_store.index.isin(top_matched)][
        ["file_name", "page_number", "chunks"]
    ]
    context = " ".join(
        vector_store[vector_store.index.isin(top_matched)]["chunks"].values
    )
    return context, top_matched_df

def answer_my_question(question):
    # get the custom relevant chunks from all the chunks in vector store.
    context, top_matched_df = get_context_from_question(
        question,
        vector_store=pdf_data_sample,
        sort_index_value=5,  # Top N results to pick from embedding vector search
    )

    # Prompt for Q&A which takes the custom context found in last step.
    prompt = f""" Answer the question using the provided context. If the answer is
              not contained in the context, say "answer not available in context" \n\n
                Context: \n {context}?\n
                Question: \n {question} \n
                Answer:
              """

    # Call the PaLM API on the prompt.
    return(text_generation_model_with_backoff(prompt=prompt))

def get_file_data():
  global pdf_data_sample
  final_data = []
 
  for file_name in files("documents/"):
      path = f"documents/{file_name}"
      _, file_type = os.path.splitext(path)
      if file_type == ".pdf":
          # loading pdf files, with page numbers as metadata.
          reader = PdfReader(path)
          for i, page in enumerate(reader.pages):
              text = page.extract_text()
              if text:
                  packet = create_data_packet(
                      file_name, file_type, page_number=int(i + 1), file_content=text)
                  final_data.append(packet)
      else:
          # loading other file types
          text = textract.process(path).decode("utf-8")
          packet = create_data_packet(
              file_name, file_type, page_number=None, file_content=text
          )
          final_data.append(packet)

  pdf_data = pd.DataFrame.from_dict(final_data)
  pdf_data = pdf_data.sort_values(
          by=["file_name", "page_number"]
  )  # sorting the datafram by filename and page_number
  pdf_data.reset_index(inplace=True, drop=True)
  pdf_data_sample = pdf_data.copy()
  # Remove all non-alphabets and numbers from the data to clean it up.
  # This is harsh cleaning. You can define your custom logic for cleansing here.
  pdf_data_sample["content"] = pdf_data_sample["content"].apply(
    lambda x: re.sub("[^A-Za-z0-9:/,\-]+", " ", x)
    )
  # Apply the chunk splitting logic here on each row of content in dataframe.
  pdf_data_sample["chunks"] = pdf_data_sample["content"].apply(split_text)
  # Now, each row in 'chunks' contains list of all chunks and hence we need to explode them into individual rows.
  pdf_data_sample = pdf_data_sample.explode("chunks")
  # Sort and reset index
  pdf_data_sample = pdf_data_sample.sort_values(by=["file_name", "page_number"])
  pdf_data_sample.reset_index(inplace=True, drop=True)
  pdf_data_sample["embedding"] = pdf_data_sample["chunks"].apply(
    lambda x: embedding_model_with_backoff([x])
    )
  pdf_data_sample["embedding"] = pdf_data_sample.embedding.apply(np.array)
  return True

class Model():
    def __init__(self):
        print(get_file_data())

    def query(self, question):
        answer = answer_my_question(question)
        return(answer)

generation_model = TextGenerationModel.from_pretrained("text-bison@001")
embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
myllm = Model()
