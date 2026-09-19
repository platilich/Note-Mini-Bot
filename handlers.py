from aiogram import Router
from aiogram.filters import Command
from aiogram import F, types
from aiogram.types import FSInputFile, LinkPreviewOptions
import asyncio
from magic_round import convert_to_round
from utils.remover import remove_old_files
from db import Users



router = Router()
db = Users()

db.init_db()



@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    nickname = message.from_user.username

    db.add_user(user_id, name, nickname)

    message_text = (
        f"Hi, <b>{name}</b>! ✨\n\n"
        "I'm a little bot that turns your videos into video notes! 🎥\n\n"
        "No subscriptions and no ads - just send a video and enjoy! 🚀\n\n"
        "☀️ <a href='https://github.com/platilich/Note-Mini-Bot'>GitHub</a>\n\n"
        "<b>Send me a video to start!</b> 💫"
    )


    await message.answer(
        message_text,
        parse_mode='HTML',
        link_preview_options=LinkPreviewOptions(is_disabled=True)
        )



@router.message(F.video | (F.document.mime_type.startswith("video/")))
async def handle_video(message: types.Message):
    is_document = message.document is not None
    video_data = message.document if is_document else message.video

    if not is_document and message.video.duration > 60:
        await message.answer("❌ The video is too long. The maximum length is 1 minute.")
        return

    processing_msg = await message.answer("🔄 Processing the video, hang on a moment...")

    input_file = f"downloads_{message.from_user.id}.mp4"
    output_file = f"output_{message.from_user.id}.mp4"


    try:
        file_info = await message.bot.get_file(video_data.file_id)
        await message.bot.download_file(str(file_info.file_path), input_file)

        success = await asyncio.to_thread(convert_to_round, input_file, output_file)

        if not success:
            await message.answer("❌ Не удалось обработать видео. Посмотри лог в терминале — теперь он там появится!")
            await processing_msg.delete()
            return


        video_note = FSInputFile(output_file)
        await message.answer_video_note(video_note)
        await processing_msg.delete()



    except Exception as e:
        await message.answer(f"⚠️ Произошла ошибка при обработке: {e}")
        if 'processing_msg' in locals():
            await processing_msg.delete()



    finally:
        remove_old_files(input_file, output_file)