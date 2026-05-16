from aiogram import Router
from aiogram.types import ErrorEvent
from utils.logger import logger

router = Router()

@router.error()
async def error_handler(event: ErrorEvent):
    logger.error('Bot error', error=str(event.exception))
    if event.update and event.update.message:
        await event.update.message.answer('⚠️ Произошла ошибка. Попробуйте позже.')