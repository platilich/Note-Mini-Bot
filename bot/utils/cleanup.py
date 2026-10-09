from os import remove
from bot.logger import logger



def remove_temp_files(files):
    try:
        for file in files:
            remove(file)

    except Exception as e:
        logger.info(e)