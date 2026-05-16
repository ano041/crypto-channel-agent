from aiogram import Router, types
from aiogram.filters import Command
from config import settings
from services.agent import generate_crypto_post
from services.moderator import send_for_approval
from utils.logger import logger

router = Router()

@router.message(Command("new_post"))
async def cmd_new_post(message: types.Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        return await message.answer("Доступ запрещён")

    topic = message.text.replace("/new_post", "").strip()
    if not topic:
        return await message.answer("Использование: /new_post Тема поста")

    status = await message.answer("🔄 Генерирую черновик...")

    try:
        post = await generate_crypto_post(topic)
        await send_for_approval(message.bot, post, message.chat.id)
        await status.edit_text("✅ Черновик отправлен на модерацию")
    except Exception as e:
        logger.error("Generation error", error=str(e))
        await status.edit_text(f"❌ Ошибка генерации: {str(e)}")