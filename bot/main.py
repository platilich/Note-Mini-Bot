import asyncio
import sys
from pathlib import Path
import os


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.handlers import router



BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

token = str(os.getenv('TOKEN'))


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())