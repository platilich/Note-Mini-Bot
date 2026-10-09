import asyncio
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import FSInputFile

from .db import Users
from .logger import logger


from utils.cleanup import remove_temp_files
from utils.video_note import convert_to_video_note
from utils.audio_recognation import transcription



router = Router()
db = Users()



@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    nickname = message.from_user.username

    if db.is_banned(user_id):
        return

    db.add_user(user_id, name, nickname)


    message_text = (
        f"Hi, <b>{name}</b>! ✨\n\n"
        "I'm a little bot that turns your videos into video notes! 🎥\n\n"
        "No subscriptions and no ads - just send a video and enjoy! 🚀\n\n"
        "☀️ <a href='https://github.com/platilich/Note-Mini-Bot'>GitHub</a>\n\n"
        "<b>Send me a video to start!</b> 💫"
    )

    await message.answer(
        text=message_text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )



@router.message(F.video | (F.document.mime_type.startswith("temp/")))
async def handle_video(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    name = message.from_user.first_name
    nickname = message.from_user.username



    if db.is_banned(user_id):
        return



    db.add_user(user_id, name, nickname)


    is_document = message.document is not None
    video_data = message.document if is_document else message.video




    if not is_document and message.video.duration > 60:
        await message.answer("❌ The video is too long. The maximum length is 1 minute.")
        return


    input_file = f"downloads_{user_id}.mp4"
    output_file = f"output_{user_id}.mp4"



    try:
        file_info = await message.bot.get_file(video_data.file_id)
        await message.bot.download_file(str(file_info.file_path), input_file)

        success = await asyncio.to_thread(convert_to_video_note, input_file, output_file)

        if not success:
            await message.answer("Unable to process. Something went wrong.")
            logger.error(f'Something went wrong')
            return


        await bot.send_chat_action(message.chat.id, action="upload_video_note")


        video_note = FSInputFile(output_file)
        await message.answer_video_note(video_note)

        db.update_count(user_id)




    except Exception as e:
        await message.answer("Unable to process. Something went wrong.")
        logger.error(f'Something went wrong {e}')


    finally:
        remove_temp_files(input_file, output_file)







@router.message(F.video_note, F.voice)
async def handle_video_note(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    name = message.from_user.first_name
    nickname = message.from_user.username


    if db.is_banned(user_id):
        return


    db.add_user(user_id, name, nickname)


    media = message.voice or message.video_note
    file_id = media.file_id



    file_path = await bot.get_file(f'temp/{user_id}_{file_id}')
    result = await asyncio.to_thread(transcription, file_path)


    try:
        await message.reply(
            f'<code>{result}</code>\n\n\n<b><a href="https://github.com/platilich/Telegram-Bot-Voice-Transcription">GitHub</a></b>',
            disable_web_page_preview=True,
            parse_mode='HTML'
        )

        db.update_count(user_id)



    except Exception as e:
        logger.error(f'error when sending a message to the user: {e}')