import whisper
from bot.logger import logger


model = whisper.load_model(name='small')

def transcription(file_path):
    try:
        logger.info('audio_recognition | recognition')


        result = model.transcribe(file_path)


        full_text = result.get('text', '').strip()

        return full_text


    except Exception as e:
        logger.error(f'audio_recognition | error: {e}')