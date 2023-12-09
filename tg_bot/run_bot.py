import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from tg_test.handlers import router


async def main_bot():
    bot = Bot(token='6918038869:AAGDb0y59pIsyMz18ZYPBpP-fQ0uYBEA9xA', parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main_bot())
