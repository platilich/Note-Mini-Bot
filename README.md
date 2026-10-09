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
ALLOWED_HOSTS=localhost,127.0.0.1
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

### Local run (development)

```bash
python manage.py runserver 0.0.0.0:8000
```

Open:

```text
http://localhost:8000/admin/
```

Log in with your superuser username and password.

## Production setup (Linux server, free domain, free HTTPS)

### Step 1: Prepare server

You need a Linux server (VPS or dedicated). You can get a free VPS from:
- **Replit** (free tier, but limited)
- **Railway** (free credits)
- **Oracle Cloud** (free tier, always free)
- **Vultr** (free $2.50/month credit, enough to test)

Or buy a cheap one from:
- **Hetzner** (€3/month)
- **DigitalOcean** (€4/month)
- **Linode** (€5/month)

SSH into your server. If using Linux (Ubuntu 20.04+):

```bash
ssh root@your_server_ip
```

### Step 2: Get a free domain

Use one of these free domain services:
- **Freenom** - free .tk domain
- **No-ip** - dynamic DNS, free
- **DuckDNS** - free subdomain
- **Cloudflare** - free domain forwarding

Or use your server's IP directly (not recommended, but works for testing).

**Example with Freenom:**
1. Go to freenom.com
2. Register free .tk domain
3. Point it to your server IP in DNS settings

**Example with DuckDNS (simpler):**
1. Go to duckdns.org
2. Create account
3. Add your domain name
4. Put your server IP
5. Your domain: `yourname.duckdns.org`

### Step 3: Install everything on server

```bash
# Update system
apt update && apt upgrade -y

# Install Python and FFmpeg
apt install -y python3.10 python3.10-venv python3-pip ffmpeg

# Install Nginx
apt install -y nginx

# Install certbot for Let's Encrypt (free HTTPS)
apt install -y certbot python3-certbot-nginx

# Create a user for the bot (optional, but better)
useradd -m -s /bin/bash videobot
su - videobot
```

### Step 4: Clone and setup bot on server

```bash
# Stay as 'videobot' user
git clone https://github.com/platilich/Note-Mini-Bot.git
cd Note-Mini-Bot

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

### Step 5: Create `.env` file

Edit `.env` with your settings:

```bash
nano .env
```

Paste this (replace with your values):

```env
TOKEN=your_telegram_bot_token_here
SECRET_KEY=your_secret_key_here_get_it_from_python_command
DEBUG=False
ALLOWED_HOSTS=yourdomain.duckdns.org,your_server_ip
```

Generate SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it in `.env`.

Save file: `Ctrl + X`, then `Y`, then `Enter`.

### Step 6: Prepare Django for production

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Enter: username, email, password

# Collect static files
python manage.py collectstatic --noinput
```

### Step 7: Setup Gunicorn socket (systemd)

Create systemd service file:

```bash
sudo nano /etc/systemd/system/videobot.service
```

Paste this (replace `videobot` if you used different user):

```ini
[Unit]
Description=VideoNoteBot Gunicorn
After=network.target

[Service]
Type=notify
User=videobot
Group=www-data
WorkingDirectory=/home/videobot/Note-Mini-Bot
Environment="PATH=/home/videobot/Note-Mini-Bot/venv/bin"
EnvironmentFile=/home/videobot/Note-Mini-Bot/.env
ExecStart=/home/videobot/Note-Mini-Bot/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/videobot.sock \
    core.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save: `Ctrl + X`, then `Y`, then `Enter`.

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable videobot
sudo systemctl start videobot

# Check status
sudo systemctl status videobot
```

### Step 8: Setup Nginx

Create Nginx config:

```bash
sudo nano /etc/nginx/sites-available/videobot
```

Paste this (replace `yourdomain.duckdns.org` with your domain):

```nginx
server {
    listen 80;
    server_name yourdomain.duckdns.org your_server_ip;

    client_max_body_size 50M;

    location / {
        proxy_pass http://unix:/run/videobot.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/videobot/Note-Mini-Bot/staticfiles/;
    }

    location /media/ {
        alias /home/videobot/Note-Mini-Bot/media/;
    }
}
```

Save: `Ctrl + X`, then `Y`, then `Enter`.

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/videobot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Get free HTTPS (Let's Encrypt)

```bash
sudo certbot --nginx -d yourdomain.duckdns.org
```

Follow the prompts. Certbot will:
1. Ask your email
2. Agree to terms
3. Automatically update Nginx config with HTTPS

Certificate auto-renews every 90 days.

### Step 10: Final check

```bash
# Check if bot service is running
sudo systemctl status videobot

# Check Nginx
sudo systemctl status nginx

# Test Nginx config
sudo nginx -t

# Check logs
sudo journalctl -u videobot -n 20
```

Open in browser:

```text
https://yourdomain.duckdns.org/admin/
```

Log in with your superuser credentials.

### Troubleshooting

**Bot not running:**
```bash
sudo journalctl -u videobot -f
```

**Nginx errors:**
```bash
sudo tail -f /var/log/nginx/error.log
```

**Certbot issues:**
```bash
sudo certbot --nginx --dry-run -d yourdomain.duckdns.org
```

**Restart everything:**
```bash
sudo systemctl restart videobot
sudo systemctl restart nginx
```

## Notes

- For production, always use HTTPS
- Keep `.env` secret and do not commit it to Git
- Certbot renews automatically
- If you use DuckDNS, keep updating your IP (it auto-updates if you refresh the page)
- Gunicorn restarts on system reboot (systemd auto-starts it)

## License

MIT. See [LICENSE](LICENSE).
