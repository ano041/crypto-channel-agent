import json
from openai import AsyncOpenAI
from config import settings
from prompts.system import CRYPTO_AGENT_PROMPT
from prompts.schemas import CryptoPostSchema
from tools.search import tavily_search
from tools.validator import crypto_validate
from memory.redis_client import save_draft
from utils.logger import logger

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_crypto_post(query: str) -> CryptoPostSchema:
    search_results = await tavily_search(query)

    messages = [
        {"role": "system", "content": CRYPTO_AGENT_PROMPT},
        {"role": "user", "content": f"""
Контекст: {json.dumps({"web_results": search_results}, ensure_ascii=False)}
Задача: {query}
        """}
    ]

    response = await client.beta.chat.completions.parse(
        model=settings.OPENAI_MODEL_MAIN,
        messages=messages,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
        response_format=CryptoPostSchema,
    )

    post: CryptoPostSchema = response.choices[0].message.parsed

    if not await crypto_validate(post):
        post.approval_status = "needs_edit"

    draft_key = post.content.headline[:60].replace(" ", "_")
    await save_draft(draft_key, post.model_dump())

    logger.info("Post generated", headline=post.content.headline, urgency=post.meta.urgency)
    return post
