import uuid
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from prompts.schemas import CryptoPostSchema
from utils.formatting import safe_md2
from memory.redis_client import save_draft


async def send_for_approval(bot: Bot, post: CryptoPostSchema, chat_id: int) -> str:
    """
    Отправка поста на модерацию с уникальным ключом.
    
    Args:
        bot: Экземпляр бота
        post: Сгенерированный пост
        chat_id: ID чата для отправки
        
    Returns:
        str: Уникальный ключ поста для callback_data
    """
    # Генерируем уникальный ключ для поста
    post_key = f"post_{uuid.uuid4().hex[:12]}"
    
    # Сохраняем черновик в Redis
    await save_draft(post_key, post.model_dump())
    
    text = f"""🆕 Новый черновик поста

*{safe_md2(post.content.headline)}*

{safe_md2(post.content.body[:1200])}...

*Тикеры:* {', '.join(post.content.tickers) or '—'}
*Сентимент:* {post.meta.sentiment} | *Срочность:* {post.meta.urgency}
*Источники:* {len(post.sources)}
*Reasoning:* {safe_md2(post.reasoning)}
"""

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"approve:{post_key}"),
            InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit:{post_key}")
        ],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{post_key}")]
    ])

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="MarkdownV2",
        reply_markup=kb
    )
    
    return post_key
