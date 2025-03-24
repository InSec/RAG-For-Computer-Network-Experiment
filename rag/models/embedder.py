# embedder.py包含文档分割、embedding模型、向量数据库、索引方法
# 知识库构建

import logging
from tqdm import tqdm
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPDFLoader,
)
from langchain_unstructured import UnstructuredLoader
from rag.models.embedding import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from rag.config import *

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_PATH1, encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class Embedder:
    def __init__(self,data_dir, vector_db_path, chunk_size, chunk_overlap, batch_size):
        self.data_dir = Path(data_dir)
        self.vector_db_path = Path(vector_db_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.batch_size = batch_size

        self._initialize()

    def _initialize(self):
        # 初始化文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""],
        )

        # 初始化向量数据库
        self.vector_db = Chroma(
            collection_name="vdb",
            persist_directory=str(self.vector_db_path),
            embedding_function=self.embedding_model,
        )

    def _get_loader(self, file_path):
        extension = file_path.suffix.lower()
        loader_map = {
            ".pdf": UnstructuredPDFLoader,
            ".docx": UnstructuredWordDocumentLoader,
            ".doc": UnstructuredWordDocumentLoader,
            ".md": UnstructuredMarkdownLoader,
        }
        return loader_map.get(extension, UnstructuredLoader)

    def _process_file(self, file_path):
        try:
            # 加载文档
            loader_class = self._get_loader(file_path)
            loader = loader_class(str(file_path), mode="elements")
            docs = loader.load()

            # 添加元数据
            for doc in docs:
                doc.metadata.update({
                    "source": str(file_path),
                    "file_name": file_path.name,
                    "file_size": f"{file_path.stat().st_size / 1024:.2f}KB",
                })

            # 分割文本
            chunks = self.text_splitter.split_documents(docs)
            return chunks

        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {str(e)}")
            return []

    def process_all(self, clean):
        # 验证数据目录
        if not self.data_dir.exists():
            raise FileNotFoundError(f"数据目录 {self.data_dir} 不存在")

        # 清理现有数据
        if clean:
            logger.warning(f"正在清除向量数据库: {self.vector_db_path}")
            self.vector_db.delete_collection()

        # 收集文件
        supported_exts = [".pdf", ".docx", ".doc", ".md", ".txt"]
        all_files = []
        for ext in supported_exts:
            all_files.extend(self.data_dir.rglob(f"*{ext}"))

        logger.info(f"发现 {len(all_files)} 个待处理文件")

        # 处理文件
        total_chunks = 0
        with tqdm(all_files, desc="处理文件") as pbar:
            for file_path in pbar:
                pbar.set_postfix(file=file_path.name[:15])

                if not file_path.is_file():
                    continue

                chunks = self._process_file(file_path)
                if chunks:
                    # 分批处理提升性能
                    for i in range(0, len(chunks), self.batch_size):
                        batch = chunks[i:i + self.batch_size]
                        self.vector_db.add_documents(batch)
                    total_chunks += len(chunks)

        logger.info(f"处理完成！共生成 {total_chunks} 个文本块")
