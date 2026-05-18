from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from aiogram import Bot
from config import settings
from memory.storage import get_draft
from tools.validator import validate_post
from utils.logger import logger

scheduler = AsyncIOScheduler(timezone="UTC")


async def publish_post(draft_key: str, bot: Bot):
    """Публикация поста в канал."""
    draft = await get_draft(draft_key)
    if not draft:
        logger.warning("Draft not found", key=draft_key)
        return

    # Валидация поста перед публикацией
    is_valid, error_msg = validate_post(draft)
    if not is_valid:
        logger.error("Post validation failed", key=draft_key, error=error_msg)
        return

    if settings.DRY_RUN:
        logger.info("DRY_RUN: post not published", key=draft_key)
        return

    try:
        content = draft["content"]
        text = f"{content.get('headline', '')}\n\n{content.get('body', '')}\n\n"
        if content.get('tickers'):
            text += ' '.join(f"${t}" for t in content['tickers']) + '\n'
        
        await bot.send_message(
            chat_id=settings.CHANNEL_ID,
            text=text,
            parse_mode='MarkdownV2'
        )
        logger.info("Post published", key=draft_key)
    except Exception as e:
        logger.error("Publish failed", key=draft_key, error=str(e))


def schedule_post(draft_key: str, delay_minutes: int = 5):
    """
    Планирование публикации поста.
    
    Args:
        draft_key: Уникальный ключ черновика
        delay_minutes: Задержка в минутах перед публикацией
    """
    run_date = datetime.now() + timedelta(minutes=delay_minutes)
    scheduler.add_job(
        publish_post, 
        'date', 
        run_date=run_date, 
        args=[draft_key],
        id=f"publish_{draft_key}",
        replace_existing=True
    )
    logger.info("Post scheduled", key=draft_key, run_at=run_date.isoformat())


def start_scheduler():
    """Запуск планировщика задач."""
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started")


def stop_scheduler():
    """Остановка планировщика задач."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")