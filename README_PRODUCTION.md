# Production Deploy — Note-Mini-Bot

This guide helps you run the bot on a Linux server (VPS). The bot will run in the background and restart automatically if it stops.

## What you need

- A Linux server (Ubuntu 20.04+, Debian 11+, etc.)
- SSH access to the server
- Python 3.10+
- FFmpeg

## Step 1: Connect to your server

```bash
ssh username@your_server_ip
```

Replace `username` and `your_server_ip` with your actual values.

## Step 2: Install requirements

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.10 python3.10-venv python3-pip ffmpeg git
```

## Step 3: Clone the bot

```bash
cd /home/your_username
git clone https://github.com/platilich/Note-Mini-Bot.git
cd Note-Mini-Bot
```

Replace `your_username` with your actual server username.

## Step 4: Create virtual environment

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 5: Create .env file

```bash
nano .env
```

Paste this:

```
TOKEN=your_telegram_bot_token_here
```

Get your bot token from [@BotFather](https://t.me/BotFather) on Telegram.

Save: press `Ctrl + X`, then `Y`, then `Enter`.

## Step 6: Test the bot

```bash
python bot/main.py
```

If you see no errors, the bot is working. Stop it: press `Ctrl + C`.

---

## Easy way (run with screen)

Use `screen` to run the bot in the background.

### Start the bot

```bash
screen -S note-mini-bot
cd /home/your_username/Note-Mini-Bot
source venv/bin/activate
python bot/main.py
```

Stop the bot: press `Ctrl + C`.

Detach from screen: press `Ctrl + A`, then `D`.

### See logs

```bash
screen -r note-mini-bot
```

### Stop the bot

```bash
screen -S note-mini-bot -X quit
```

**Problem:** Bot stops if you restart the server. Use the better way below.

---

## Better way (auto start with systemd)

The bot will start automatically when the server starts.

### Step 1: Create service file

```bash
sudo nano /etc/systemd/system/note-mini-bot.service
```

### Step 2: Paste this text

Replace these:
- `your_username` — your server username
- `/home/your_username/Note-Mini-Bot` — full path to the bot directory

```ini
[Unit]
Description=Note Mini Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/Note-Mini-Bot
EnvironmentFile=/home/your_username/Note-Mini-Bot/.env
ExecStart=/home/your_username/Note-Mini-Bot/venv/bin/python bot/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Save: press `Ctrl + X`, then `Y`, then `Enter`.

### Step 3: Enable auto start

```bash
sudo systemctl daemon-reload
sudo systemctl enable note-mini-bot
sudo systemctl start note-mini-bot
```

Done. The bot now runs in the background and restarts automatically.

### Check status

```bash
sudo systemctl status note-mini-bot
```

You should see: `active (running)`.

### See live logs

```bash
sudo journalctl -u note-mini-bot -f
```

Stop viewing: press `Ctrl + C`.

### See last 50 lines of logs

```bash
sudo journalctl -u note-mini-bot -n 50
```

### Restart the bot

```bash
sudo systemctl restart note-mini-bot
```

### Stop the bot

```bash
sudo systemctl stop note-mini-bot
```

### Start the bot

```bash
sudo systemctl start note-mini-bot
```

---

## Environment variables (.env)

The `.env` file must have this:

```
TOKEN=your_telegram_bot_token_here
```

Optional:

```
DEBUG=False
FFMPEG_PATH=/usr/bin/ffmpeg
```

If FFmpeg is not found, set `FFMPEG_PATH` to the full path to the `ffmpeg` binary:

```bash
which ffmpeg
```

This shows you the path.

---

## What you do NOT need for the bot to work

- Nginx (web server)
- Gunicorn (Python server)
- Domain name
- HTTPS / SSL certificate

**These are only needed if you want to use the Django admin page** (optional feature to manage data).

The bot works fine without them.

---

## Troubleshooting

### Bot does not start

Check logs:

```bash
sudo journalctl -u note-mini-bot -n 20
```

Common problems:

- **Token is wrong** — check `.env`, get a new token from @BotFather
- **FFmpeg not installed** — run `sudo apt install ffmpeg`
- **Wrong path in service file** — check that the path to the bot folder is correct
- **Permission error** — make sure `User=` in service file matches your username

### Bot crashes after restart

Restart the service:

```bash
sudo systemctl restart note-mini-bot
```

Check logs to see why it crashed:

```bash
sudo journalctl -u note-mini-bot -n 50
```

### Check if bot is running

```bash
ps aux | grep python
```

Look for `bot/main.py` in the output.

---

## Optional: Django Admin (if needed)

If you want to manage data using Django admin (optional), you need extra steps. See the main README.md for details.

---

## That's it!

Your bot is now running in production. It will:
- Run in the background
- Restart if it crashes
- Start automatically when the server reboots

Good luck!
