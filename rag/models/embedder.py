# embedder.py包含文档分割、embedding模型、向量数据库、索引方法
# 知识库构建

import os
from sentence_transformers import SentenceTransformer
import json


class Embedder:
    def __init__(self, model_name, storage_path):
        self.model = SentenceTransformer(model_name)
        self.storage_path = storage_path

    def embeddings(self, data_path):
        return None

    def load_embeddings(self):
        return None

