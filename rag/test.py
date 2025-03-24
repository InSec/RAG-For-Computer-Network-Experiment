from rag import RAG


if __name__ == '__main__':
    rag = RAG()
    query = '介绍下艾尔登法环。'
    rag.answer_query(query)
