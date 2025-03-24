# RAG

from models.retriever import Retriever
from models.generator import Generator
from config import *


class RAG:
    def __init__(self,):
        self.config1 = {
            "vector_db_path": VECTOR_DB_PATH,
            "model_name": RETRIEVE_MODEL,
            "extra_query": EXTRA_QUERY,
            "top_k": TOP_K,
        }
        self.config2 = {
            'model_name': GENERATE_MODEL,
            'api_key': API_KEY,
            'base_url': BASE_URL
        }
        self.retriever = Retriever(**self.config1)
        self.generator = Generator(**self.config2)

    def answer_query(self, query):
        context = self.retriever.retrieve(query)
        answer = self.generator.generate_ds(query, context)

        return answer
