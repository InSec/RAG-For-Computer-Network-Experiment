# RAG

from models.embedder import Embedder
from models.retriever import Retriever
from models.generator import Generator


class RAG:
    def __init__(self, api_key):
        # 加载知识库
        embedder = Embedder()
        self.texts, self.embeddings = embedder.load_embeddings()
        self.retriever = Retriever()
        self.generator = Generator(api_key)

    def answer_query(self, query, top_k=3):
        # 查询向量化
        embedder = Embedder()
        query_embedding = embedder.model.encode(query)

        # 检索相关内容
        results = self.retriever.retrieve(query_embedding, top_k=top_k)
        context = "\n".join([text for text, _ in results])

        # 生成回答
        answer = self.generator.generate(query, context)
        return answer
