from aiogram import executor
from app.bot import bot
import logging
from app.handlers.handlers import dp, cmd_start


logging.basicConfig(level=logging.INFO)

dp.register_message_handler(cmd_start)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
