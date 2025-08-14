from langchain_openai import ChatOpenAI
from llm.chain import GeneralChain
from llm.prompt_templates import SelfQueryTemplate
from config import settings


class SelfQuery:
    @staticmethod
    def generate_response(query: str) -> str | None:
        prompt = SelfQueryTemplate().create_template()
        # 修改这里，使用Qwen模型
        model = ChatOpenAI(
            model=settings.QWEN_MODEL_ID,
            api_key=settings.QWEN_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            temperature=0
        )

        chain = GeneralChain().get_chain(
            llm=model, output_key="metadata_filter_value", template=prompt
        )

        response = chain.invoke({"question": query})
        result = response.get("metadata_filter_value", "none")
        
        if result.lower() == "none":
            return None

        return result
