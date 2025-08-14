from config import settings
from langchain_openai import ChatOpenAI

from core.rag.prompt_templates import RerankingTemplate


class Reranker:
    @staticmethod
    def generate_response(
        query: str, passages: list[str], keep_top_k: int
    ) -> list[str]:
        reranking_template = RerankingTemplate()
        prompt = reranking_template.create_template(keep_top_k=keep_top_k)
        # 修改这里，使用Qwen模型
        model = ChatOpenAI(
            model=settings.QWEN_MODEL_ID,
            api_key=settings.QWEN_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        chain = prompt | model

        stripped_passages = [
            stripped_item for item in passages if (stripped_item := item.strip())
        ]
        passages = reranking_template.separator.join(stripped_passages)
        response = chain.invoke({"question": query, "passages": passages})
        response = response.content

        reranked_passages = response.strip().split(reranking_template.separator)
        stripped_passages = [
            stripped_item
            for item in reranked_passages
            if (stripped_item := item.strip())
        ]

        return stripped_passages
