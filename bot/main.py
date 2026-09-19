import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
from pathlib import Path
import os



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