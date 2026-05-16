import json
import redis.asyncio as aioredis
from config import settings
from utils.logger import logger

redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def init_redis():
    try:
        await redis_client.ping()
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.error("Redis connection failed", error=str(e))

async def save_draft(key: str, data: dict, expire: int = 7200):
    await redis_client.setex(f"draft:{key}", expire, json.dumps(data))

async def get_draft(key: str) -> dict | None:
    data = await redis_client.get(f"draft:{key}")
    return json.loads(data) if data else None