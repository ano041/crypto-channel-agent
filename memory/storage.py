import json
from typing import Optional, Dict, Any
from utils.logger import logger

# In-memory storage (fallback if Redis is unavailable)
_memory_store: Dict[str, str] = {}

async def init_redis():
    """Try to initialize Redis, fallback to memory if failed."""
    try:
        from memory.redis_client import redis_client
        await redis_client.ping()
        logger.info("Redis connected successfully")
        return True  # Redis is available
    except Exception as e:
        logger.warning(f"Redis connection failed ({e}), using in-memory storage instead")
        logger.warning("Note: Drafts and scheduled posts will be lost on restart")
        return False  # Fallback to memory

async def save_draft(key: str, data: dict, expire: int = 7200):
    """Save draft to Redis or in-memory storage."""
    try:
        from memory.redis_client import redis_client
        # Try Redis first
        try:
            await redis_client.ping()
            await redis_client.setex(f"draft:{key}", expire, json.dumps(data))
            return
        except:
            pass  # Fall through to memory storage
    except ImportError:
        pass
    
    # Fallback to in-memory
    _memory_store[f"draft:{key}"] = json.dumps(data)
    logger.debug(f"Draft saved to memory: {key}")

async def get_draft(key: str) -> Optional[dict]:
    """Get draft from Redis or in-memory storage."""
    try:
        from memory.redis_client import redis_client
        # Try Redis first
        try:
            await redis_client.ping()
            data = await redis_client.get(f"draft:{key}")
            if data:
                return json.loads(data)
        except:
            pass  # Fall through to memory storage
    except ImportError:
        pass
    
    # Fallback to in-memory
    data = _memory_store.get(f"draft:{key}")
    if data:
        logger.debug(f"Draft loaded from memory: {key}")
        return json.loads(data)
    return None
