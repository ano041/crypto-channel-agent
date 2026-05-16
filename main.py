import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import settings
from memory.redis_client import init_redis
from handlers.commands import router as commands_router
from handlers.callbacks import router as callbacks_router
from handlers.errors import router as errors_router
from utils.logger import logger

async def on_startup(bot: Bot):
    await init_redis()
    logger.info("Bot started", username=(await bot.get_me()).username)

async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    dp = Dispatcher()

    dp.include_routers(commands_router, callbacks_router, errors_router)
    dp.startup.register(on_startup)

    logger.info("Starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())