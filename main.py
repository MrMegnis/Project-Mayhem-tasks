import asyncio

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

import settings
from utils.logger import logger
from bot.handlers.user_handlers import rt
from bot.handlers.callbacks import callback_router


async def main():
    logger.info('Starting bot')
    bot = Bot(token=settings.get_settings('.env').bots.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(rt, callback_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot Stopped!')
