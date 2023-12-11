import asyncio

from aiogram import Bot, Dispatcher

from settings import get_settings
from utils.logger import logger


async def start_bot(bot: Bot):
    pass


async def stop_bot(bot: Bot):
    pass


def register_all_handlers(dp: Dispatcher):
    dp.startup.register(start_bot)


async def main():
    logger.info('Starting bot')

    settings = get_settings('.env')

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    register_all_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot Stopped!')
