# generator.py根据问题、检索得到的上下文生成答案，包含llm、提示词、历史对话
# 答案生成

from openai import OpenAI


class Generator:
    def __init__(self, model_name, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.model = OpenAI(api_key=api_key, base_url=base_url)


    def get_prompt(self, query, context):
        # 提示词设定
        prompt = f"问题: {query}\n\n"
        prompt += "上下文:\n"
        for i, doc in enumerate(context):
            prompt += f"文档 {i + 1}:\n{doc.page_content}\n\n"
        prompt += ("对于提出的问题，请首先基于给定的上下文，结合你已有的相关知识，给出准确全面、符合要求的回答。当上下文确实或上下文"
                   "与问题无关、完全无法用于问题的解答时，可以灵活变通，忽略上下文。\n")
        prompt += "答案:"

        return prompt

    def generate_ds(self, query, context):
        prompt = self.get_prompt(query, context)
        print(prompt)
        # 答案生成
        response = self.model.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "你是一个计算机网络领域专家，帮助回答计算机网络课程及其实验的相关问题并给予学生学习指导。"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        result = response.choices[0].message.content
        print(result)

        return result
