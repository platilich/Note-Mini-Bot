# VideoNoteBot

This is a small Telegram bot. It turns a video into a round video note.

It is made with Python, aiogram, FFmpeg, and Django admin.

## What it does

- Send a video and get a round video note
- Send a voice message or video note and get text
- Videos longer than 60 seconds are not accepted
- Temporary files are removed after conversion
- You can also use Django admin to manage the project

## Screenshots

<table>
  <tr>
    <td><img src="screenshots/start.png" alt="Photo showing how the /start command works" width="400"/></td>
    <td align="center"><img src="screenshots/conversion.jpeg" alt="Example: send a video and get a transcript" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>/start</b></td>
    <td align="center"><b>Send a Video → Get a video note</b></td>
  </tr>
  <tr>
    <td align="center"><img src="screenshots/fourth.jpeg" alt="Example of voice message transcription" width="400"/></td>
    <td align="center"><img src="screenshots/third.png" alt="Example of video note transcription" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><b>Voice Message Transcription</b></td>
    <td align="center"><b>Video Note Transcription</b></td>
  </tr>
</table>

## Requirements

- Python 3.10+
- FFmpeg
- Telegram bot token from @BotFather
- Docker (optional, for Docker setup)

## Install FFmpeg

### macOS

```bash
brew install ffmpeg
```

### Windows

```powershell
winget install --id Gyan.FFmpeg
```

### Linux

```bash
sudo apt install ffmpeg
```

Check:

```bash
ffmpeg -version
```

If FFmpeg is not in PATH, set this in `.env`:

```env
FFMPEG_PATH=/usr/bin/ffmpeg
```

## Run locally

Clone the project:

```bash
git clone https://github.com/platilich/Note-Mini-Bot.git
cd Note-Mini-Bot
```

Create a virtual environment:

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` in the project root:

```env
TOKEN=your_telegram_bot_token
SECRET_KEY=your_django_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then run the bot:

```bash
python bot/main.py
```

Open Telegram and send `/start`.

## Django admin

You can use Django admin for management.

Create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

You will be asked for:

- username
- email
- password

Then run the admin:

### Local run

```bash
python manage.py runserver 0.0.0.0:8000
```

Open:

```text
http://localhost:8000/admin/
```

Log in with your superuser username and password.

### HTTPS

For production, do not use `runserver` directly.

Use a real web server with HTTPS, for example:

- Nginx
- Apache
- Traefik
- Let's Encrypt

A simple setup is:

1. Run Django with Gunicorn
2. Put Nginx in front of it
3. Add SSL with Let's Encrypt

Example:

```bash
pip install gunicorn

gunicorn --bind 0.0.0.0:8000 --workers 4 core.wsgi:application
```

Then set up Nginx to proxy to `127.0.0.1:8000` and enable HTTPS.

Important:

```env
ALLOWED_HOSTS=yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

## Docker

You can also run the project with Docker.

Example:

```bash
docker build -t videonotebot .
docker run --env-file .env -p 8000:8000 videonotebot
```

If you use Docker Compose, make a file called `docker-compose.yml` like this:

```yaml
version: '3.9'

services:
  app:
    build: .
    env_file:
      - .env
    ports:
      - "8000:8000"
    command: python manage.py runserver 0.0.0.0:8000
```

Then run:

```bash
docker compose up --build
```

Open:

```text
http://localhost:8000/admin/
```

## Notes

- For a real production site, use HTTPS and a domain name.
- Keep `.env` secret.
- Do not use the Django development server in public production.

## License

MIT. See [LICENSE](LICENSE).
