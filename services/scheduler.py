from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from aiogram import Bot
from config import settings
from memory.redis_client import get_draft
from utils.logger import logger

scheduler = AsyncIOScheduler(timezone="UTC")

async def publish_post(draft_key: str, bot: Bot):
    draft = await get_draft(draft_key)
    if not draft:
        logger.warning("Draft not found", key=draft_key)
        return

    if settings.DRY_RUN:
        logger.info("DRY_RUN: post not published")
        return

    try:
        content = draft["content"]
        text = f"{content.get('headline', '')}\n\n{content.get('body', '')}\n\n"
        if content.get('tickers'):
            text += ' '.join(content['tickers']) + '\n'
        await bot.send_message(
            chat_id=settings.CHANNEL_ID,
            text=text,
            parse_mode='MarkdownV2'
        )
        logger.info("Post published", key=draft_key)
    except Exception as e:
        logger.error("Publish failed", error=str(e))

def schedule_post(draft_key: str, delay_minutes: int = 5):
    scheduler.add_job(publish_post, 'date', run_date=datetime.utcnow(), args=[draft_key])