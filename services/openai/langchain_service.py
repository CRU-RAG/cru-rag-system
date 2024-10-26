import os
from langchain_openai import ChatOpenAI


class LangChainService:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url="https://api.openai.com/v1/",
            model="gpt-4o-mini",
            api_key=os.environ.get("OPENAI_API_KEY"),
            temperature=0.9,
        )

    def chat(self, chat_messages):
        return self.llm.invoke(chat_messages).content
