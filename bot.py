from aiogram import Bot, types
from utils import config


bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=types.ParseMode.HTML)
