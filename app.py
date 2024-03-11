""" import json
import textwrap
# Utils
import time
import vertexai
import uuid
import numpy as np
from typing import List
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import GCSDirectoryLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import matching_engine
from google.cloud import aiplatform



vertexai.init(project="cs470-rag-llm",location="us-central1")

# utility functions that we will use for the Vertex AI Embeddings API

def rate_limit(max_per_minute):
    period = 60 / max_per_minute
    print("Waiting")
    while True:
        before = time.time()
        yield
        after = time.time()
        elapsed = after - before
        sleep_time = max(0, period - elapsed)
        if sleep_time > 0:
            print(".", end="")
            time.sleep(sleep_time)

class CustomVertexAIEmbeddings(VertexAIEmbeddings):
    requests_per_minute: int
    num_instances_per_batch: int
    
    # Overriding embed_documents method
    def embed_documents(self, texts: List[str]):
        limiter = rate_limit(self.requests_per_minute)
        results = []
        docs = list(texts)
        
        while docs:
            # Working in batches because the API accepts maximum 5 documents per request to get embeddings
            head, docs = (
                docs[: self.num_instances_per_batch],
                docs[self.num_instances_per_batch :],
            )
            chunk = self.client.get_embeddings(head)
            results.extend(chunk)
            next(limiter)
        
        
        return [r.values for r in results]
# Text model instance integrated with langChain
llm = VertexAI(
    model_name="text-bison@002",
    max_output_tokens=1024,
    temperature=0.2,
    top_p=0.8,
    top_k=40,
    verbose=True,
)

# Embeddings API integrated with langChain
EMBEDDING_QPM = 100
EMBEDDING_NUM_BATCH = 5
embeddings = CustomVertexAIEmbeddings(
    requests_per_minute=EMBEDDING_QPM,
    num_instances_per_batch=EMBEDDING_NUM_BATCH,
)

# can declare as variables in terminal itself
ME_REGION = "us-central1"
ME_INDEX_NAME = "cs470-rag-llm-me-index"
ME_EMBEDDING_DIR = "cs470-rag-llm-me-bucket"
ME_DIMENSIONS = 768


# dummy embedding
init_embedding = {"id": str(uuid.uuid4()), "embedding": list(np.zeros(ME_DIMENSIONS))}

# dump embedding to a local file
with open("embeddings_0.json", "w") as f:
    json.dump(init_embedding, f)


aiplatform.init(project="cs470-rag-llm", location="us-central1", staging_bucket="gs://pdx_test_bucket")

my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name="pdx-cs-ask-index",
    contents_delta_uri="gs://cs470-rag-llm-me-bucket/init_index",
    dimensions=ME_DIMENSIONS,
    approximate_neighbors_count=150,
    distance_measure_type="DOT_PRODUCT_DISTANCE",
)

my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name="pdx-cs-ask-endpoint",
    public_endpoint_enabled=True,
)

my_index_endpoint.deploy_index(deployed_index_id="endpoint_test",index=my_index) """


