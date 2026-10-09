# VideoNoteBot

A small Telegram bot that turns any video into a round video note. Send a video, get a circle back. No ads, no subscriptions.

Built with [aiogram 3](https://docs.aiogram.dev/) and [FFmpeg](https://ffmpeg.org/).

## Features

- Send a video (or a video file) and get a round video note
- Send voice messages or video notes and get instant transcripts
- Videos longer than 60 seconds are rejected (Telegram limit)
- Temporary files are deleted after conversion

## Screenshots

<table>
    <tr>
        <td><img src="screenshots/start.png" alt="Photo showing how the /start command works" width="400"/></td>
        <td align="center"><img src="screenshots/conversion.jpeg" alt="Example: send a video and get a transcript" width="400"/></td>
    </tr>
    <tr>
        <td align="center"><b>/start</b></td>
        <td align="center"><b>Send a Video -> Get a video note</b></td>
    </tr>
    <tr>
        <td align="center"><img src="screenshots/third.png" alt="Example of voice message transcription" width="400"/></td>
        <td align="center"><img src="screenshots/fourth.jpeg" alt="Example of video note transcription" width="400"/></td>
    </tr>
    <tr>
        <td align="center"><b>Voice Message Transcription</b></td>
        <td align="center"><b>Video Note Transcription</b></td>
    </tr>
</table>


## Requirements

- Python 3.10+
- FFmpeg
- A bot token from [@BotFather](https://t.me/BotFather)

## Install FFmpeg

**macOS**

```bash
brew install ffmpeg
```

**Windows**

```powershell
winget install --id Gyan.FFmpeg
```

**Linux**

```bash
sudo apt install ffmpeg
```

Then check that it works:

```bash
ffmpeg -version
```

If `ffmpeg` is not on your PATH, set `FFMPEG_PATH` in `.env` (see below).

## Setup

```bash
git clone https://github.com/platilich/Note-Mini-Bot.git
cd Note-Mini-Bot
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optional, if FFmpeg is not on PATH:

```
FFMPEG_PATH=C:\ffmpeg\bin\ffmpeg.exe
```


### Set up .env
Create a `.env` file in the project root:

```
TOKEN=your_telegram_bot_token
```

Generate secret token for django:

``
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
``

Past your secret key like this:

```
SECRET_KEY=your_secret_key
```


Run the bot:

```bash
python bot/main.py
```

Open the bot in Telegram, send /start, then try sending a video note, voice message, or video.

## License

MIT. See [LICENSE](LICENSE).