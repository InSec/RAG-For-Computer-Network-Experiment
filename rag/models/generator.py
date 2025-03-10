# generator.py根据问题、检索得到的上下文生成答案，包含llm、提示词工程、历史对话
# 答案生成

import openai


class Generator:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate(self, query, context):
        return None
