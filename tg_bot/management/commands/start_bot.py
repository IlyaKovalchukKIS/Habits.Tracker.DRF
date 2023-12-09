import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from django.core.management import BaseCommand

from config.settings import TG_BOT_TOKEN
from tg_bot.handlers import router


async def main_bot():
    bot = Bot(token=TG_BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main_bot())
