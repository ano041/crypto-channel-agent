from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from prompts.schemas import CryptoPostSchema
from utils.formatting import safe_md2

async def send_for_approval(bot: Bot, post: CryptoPostSchema, chat_id: int):
    text = f"""🆕 **Новый черновик поста**

**{post.content.headline}**

{post.content.body[:1200]}...

**Тикеры:** {', '.join(post.content.tickers) or '—'}
**Сентимент:** {post.meta.sentiment} | **Срочность:** {post.meta.urgency}
**Источники:** {len(post.sources)}
**Reasoning:** {post.reasoning}
"""

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"approve:{id(post)}"),
            InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit:{id(post)}")
        ],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{id(post)}")]
    ])

    await bot.send_message(
        chat_id=chat_id,
        text=safe_md2(text),
        parse_mode="MarkdownV2",
        reply_markup=kb
    )
