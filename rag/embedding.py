from models.embedder import Embedder
from rag.config import *
import os
os.environ["TP_NUM_C_BUFS"] = "100"


if __name__ == '__main__':
    _config = {
        "data_dir":DATA_DIR,
        "vector_db_path":VECTOR_DB_PATH,
        "chunk_size":CHUNK_SIZE,
        "chunk_overlap":CHUNK_OVERLAP,
        "batch_size":BATCH_SIZE,
    }

    embedder = Embedder(**_config)

    embedder.process_all(clean=True)
