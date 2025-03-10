# retriever.py包含用户意图理解（对原始query进行扩展）、检索向量数据库获取上下文（检索算法）、检索结果的处理（重排等）
# 用户意图理解

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Retriever:
    def __init__(self, texts, embeddings):
        self.texts = texts
        self.embeddings = np.array(embeddings)

    def retrieve(self):

        return None
