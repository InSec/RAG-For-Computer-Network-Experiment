# retriever.py包含用户意图理解（对原始query进行扩展）、检索向量数据库获取上下文（检索算法）、检索结果的处理（重排等）
# 用户意图理解

import logging
from langchain_chroma import Chroma
from rag.models.embedding import embedding_model
from rag.config import *
from tqdm import tqdm

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_PATH2, encoding="utf-8"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self, vector_db_path, model_name, extra_query, top_k):
        self.vector_db_path = vector_db_path
        self.model_name = model_name
        self.extra_query = extra_query
        self.top_k = top_k

        # 初始化组件
        self._initialize()

    def _initialize(self):
        # 向量数据库
        self.vector_db = Chroma(
            persist_directory=str(self.vector_db_path),
            embedding_function=embedding_model,
        )




    def get_rewrite_prompt(self, query):
        prompt = f"问题: {query}\n\n"
        prompt += ("对提出的问题进行重写，要求不改变原问题意思，修正不正确的字或句式。同时结合计算机网络课程和实验内容的知识，"
                   "检查并更正错误的术语。\n")
        prompt += "结果:"
        return prompt

    def rewrite_query(self, query):
        try:
            prompt = self.get_rewrite_prompt(query)
            # 查询重写

            return query
        except Exception as e:
            logger.error(f"查询重写失败: {str(e)}")
            return query

    def get_expand_prompt(self, query):
        prompt = f"问题: {query}\n\n"
        prompt += (" \n")
        prompt += "结果:"
        return prompt

    def expand_query(self, query):
        try:
            prompt = self.get_expand_prompt(query)
            # 扩展查询
            expanded = []
            return [query] + expanded
        except Exception as e:
            logger.error(f"查询扩展失败: {str(e)}")
            return [query]

    def _retrieve_single(self, query, k):
        """单次检索"""
        try:
            return self.vector_db.similarity_search(query, k=k)
        except Exception as e:
            logger.error(f"检索失败: {str(e)}")
            return []

    def _weighted_rerank(self, all_results):
        """加权重排序"""
        doc_scores = {}
        for i, results in enumerate(all_results):
            for rank, doc in enumerate(results):
                score = 1.0 / (rank + 1 + i * 0.1)  # 越靠前的查询权重越高
                if doc.metadata["source"] in doc_scores:
                    doc_scores[doc.metadata["source"]] += score
                else:
                    doc_scores[doc.metadata["source"]] = score

        # 按总分排序
        sorted_docs = sorted(
            {doc for results in all_results for doc in results},
            key=lambda x: doc_scores[x.metadata["source"]],
            reverse=True
        )
        return sorted_docs[:self.top_k]

    def _rrf_rerank(self, all_results):
        """倒数排序融合 (Reciprocal Rank Fusion)"""
        rrf_scores = {}
        k = 60  # RRF常数

        for results in all_results:
            for rank, doc in enumerate(results):
                score = 1.0 / (k + rank)
                key = f"{doc.metadata['source']}-{doc.page_content[:50]}"
                rrf_scores[key] = rrf_scores.get(key, 0) + score

        # 去重并排序
        seen = set()
        unique_docs = []
        for results in all_results:
            for doc in results:
                key = f"{doc.metadata['source']}-{doc.page_content[:50]}"
                if key not in seen:
                    seen.add(key)
                    unique_docs.append((doc, rrf_scores.get(key, 0)))

        return [doc for doc, _ in sorted(unique_docs, key=lambda x: -x[1])][:self.top_k]

    def retrieve(self, query):
        """检索流程"""
        '''
        # 1. 查询重写
        rewritten_query = self.rewrite_query(query)
        logger.info(f"重写后查询: {rewritten_query}")

        # 2. 查询扩展
        expanded_queries = self.expand_query(rewritten_query)
        logger.info(f"扩展查询: {expanded_queries}")

        # 3. 多路检索
        all_results = []
        base_k = self.top_k * 2  # 每路检索数量

        for query in tqdm(expanded_queries, desc="多路检索"):
            results = self._retrieve_single(query, k=base_k)
            all_results.append(results)

        # 4. 结果融合
        final_results = self._rrf_rerank(all_results)

        # 5. 去重处理
        seen = set()
        unique_results = []
        for doc in final_results:
            key = f"{doc.metadata['source']}-{hash(doc.page_content)}"
            if key not in seen:
                seen.add(key)
                unique_results.append(doc)

        return unique_results[:self.top_k]
        '''
        return self._retrieve_single(query, k=self.top_k)
