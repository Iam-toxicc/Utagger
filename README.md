# UserTagger Pro

Premium Telegram User Tagger Bot.

## Features

- TagAll
- Admin Tag
- Broadcast
- Stats
- Force Join
- MongoDB
- Premium UI
- Callback Settings

## Install

```bash
git clone <repo>
cd UserTagger-Pro

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
nano .env

python3 main.py
```

PM2

```bash
pm2 start main.py --interpreter venv/bin/python --name UserTagger
pm2 save
```
