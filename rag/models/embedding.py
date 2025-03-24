from rag.config import *
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.embeddings import DashScopeEmbeddings


embedding_model = DashScopeEmbeddings(model='text-embedding-v1',
                                 dashscope_api_key="sk-1f7f512bd00a478aa3542da6da63aca3")

'''
embedding_model = SentenceTransformerEmbeddings(
    model_name=EMBED_MODEL,
    model_kwargs={"device": DEVICE},
    encode_kwargs={
        "batch_size": BATCH_SIZE,
        "convert_to_tensor": False,
        "show_progress_bar": True,
        "normalize_embeddings": True,
        'convert_to_numpy': True,
    }
)
'''
