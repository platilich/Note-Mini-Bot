from os import remove
from utils.logger import logger

def remove_old_files(input_file, output_file):
    try:
        remove(input_file)

    except Exception as e:
        logger.info(e)

    try:
        remove(output_file)

    except Exception as e:
        logger.info(e)