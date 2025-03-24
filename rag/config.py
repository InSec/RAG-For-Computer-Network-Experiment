from pathlib import Path
import torch

# Embedding
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RETRIEVE_MODEL = ''
DEVICE = "cuda" if torch.cuda.is_available() else 'cpu'
BATCH_SIZE = 8

# 数据路径
ROOT_PATH = Path(__file__).parent.absolute()
DATA_DIR = ROOT_PATH/"data"/"raw_data"
VECTOR_DB_PATH = ROOT_PATH/"vector_db"
LOG_PATH1 = ROOT_PATH / "log" / "embedder.log"
LOG_PATH2 = ROOT_PATH / "log" / "retriever.log"
CACHE_PATH = ROOT_PATH/"cache"

# 文本分割
CHUNK_SIZE = 128
CHUNK_OVERLAP = 16

# RAG参数
EXTRA_QUERY = 3
TOP_K = 5  # 检索文档数量

# LLM
# GENERATE_MODEL = 'deepseek-chat'
# API_KEY = 'sk-d8580b2930a143cbacbc2d8173f827c7'
# BASE_URL = "https://api.deepseek.com/v1"
GENERATE_MODEL = 'qwen-plus'
API_KEY = 'sk-1f7f512bd00a478aa3542da6da63aca3'
BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
