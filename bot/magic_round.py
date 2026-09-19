from logger import logger
import subprocess
import sys
import os



def convert_to_round(input_path: str, output_path: str) -> bool:
    # Use ffmpeg from PATH so the bot works on any OS.
    # You can override it with the FFMPEG_PATH env variable if needed.
    ffmpeg_path = os.getenv("FFMPEG_PATH", "ffmpeg")

    cmd = [
        ffmpeg_path, "-y", "-i", input_path,
        "-map", "0:v:0",
        "-map", "0:a:1?",
        "-map", "0:a:0?",
        "-ignore_unknown", # ignore apple_apac
        "-vf", "scale=640:640:force_original_aspect_ratio=increase,crop=640:640",
        "-t", "60",
        "-c:v", "libx264",
        "-profile:v", "baseline",
        "-level", "3.0",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-ar", "44100",
        "-b:a", "128k",
        output_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not (os.path.exists(output_path) and os.path.getsize(output_path) > 0):
        print("\n=== ERROR FFMPEG ===", file=sys.stderr)
        print(result.stderr.decode('utf-8'), file=sys.stderr)
        print("=====================\n", file=sys.stderr)
        logger.error(result.stderr.decode('utf-8'))

        return False

    return True