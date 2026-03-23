# 📒 NoteBot StarterKit

> A **production-ready StarterKit** for building Telegram bots and Mini Apps.
> Fork it, rename it, swap the domain logic — everything else is already wired up.

![Version](https://img.shields.io/badge/version-2.0.0-purple?style=flat-square)
![aiogram](https://img.shields.io/badge/aiogram-3.x-blue?style=flat-square)
![MongoDB](https://img.shields.io/badge/MongoDB-Motor-green?style=flat-square)
![Vue](https://img.shields.io/badge/Vue-3-brightgreen?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-teal?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-orange?style=flat-square)

---

## ✨ What You Get

| Layer | Tech | Purpose |
|-------|------|---------|
| **Bot** | aiogram 3 (async) | Telegram bot commands + inline mode |
| **API** | FastAPI + Vercel | Webhook receiver + REST API for Mini App |
| **Database** | MongoDB (Motor async) | Notes + user storage |
| **Frontend** | Vue 3 + Tailwind CSS v4 | Telegram Mini App (WebApp) |
| **Auth** | Telegram initData HMAC | Secure Mini App ↔ API communication |
| **Deploy** | Vercel (serverless) | Zero-config production hosting |

---

## 🏗️ Project Structure

```
.
├── config.py                    # Central config – reads from .env
├── main.py                      # Entry point for local polling mode
├── sample.env                   # Copy → .env, fill in values
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js / Vite dependencies
├── vercel.json                  # Vercel serverless + SPA routing
├── pyvuebot.json                # Project metadata
│
├── bot/                         # 🤖 Bot package (plugin-based)
│   ├── __init__.py              #    load_all_plugins(dp)
│   ├── __main__.py              #    python -m bot  (polling)
│   ├── core/
│   │   ├── bot.py               #    aiogram Bot + Dispatcher singleton
│   │   └── mongo.py             #    Motor client + index creation
│   ├── plugins/
│   │   ├── bot/
│   │   │   ├── start.py         #    /start  (opens Mini App WebApp button)
│   │   │   ├── help.py          #    /help
│   │   │   └── inline.py        #    @bot <search> inline mode
│   │   ├── notes/
│   │   │   ├── add.py           #    /addnote
│   │   │   ├── list.py          #    /notes
│   │   │   ├── view.py          #    /note <id>  + pin callback
│   │   │   ├── delete.py        #    /delnote <id>
│   │   │   └── search.py        #    /search <query>
│   │   └── sudo/
│   │       └── stats.py         #    /stats  (admin only)
│   └── utils/
│       ├── logger.py            #    Structured logging
│       ├── formatters.py        #    HTML message formatters
│       ├── database/
│       │   ├── users.py         #    User CRUD (MongoDB)
│       │   └── notes.py         #    Notes CRUD (MongoDB)
│       └── decorators/
│           └── admins.py        #    @admin_only decorator
│
├── api/                         # 🌐 FastAPI app (Vercel entry point)
│   ├── index.py                 #    App factory + lifespan
│   ├── middleware/
│   │   └── auth.py              #    Telegram initData validation
│   └── routes/
│       ├── telegram.py          #    POST /api/telegram/webhook
│       └── notes.py             #    REST /api/notes/*
│
├── src/                         # 🎨 Vue 3 Telegram Mini App
│   ├── App.vue                  #    Root: note list + search + modals
│   ├── main.js
│   ├── style.css                #    Tailwind v4 + CSS vars + dark theme
│   ├── services/
│   │   ├── telegramService.js   #    WebApp SDK wrapper
│   │   └── apiService.js        #    Authenticated fetch helpers
│   ├── store/
│   │   └── notes.js             #    Vue composable (useNoteStore)
│   └── components/
│       ├── UserInfo.vue         #    Avatar + name + note count
│       ├── NoteList.vue         #    List of NoteCards
│       ├── NoteCard.vue         #    Single note (preview, pin, delete)
│       └── NoteForm.vue         #    Bottom-sheet "New Note" form
│
└── strings/                     # 🌍 i18n string files
    ├── helpers.py               #    load_strings / get_string
    └── langs/
        └── en.yml               #    English bot messages
```

---

## 🚀 Quick Start

### 1 – Clone & configure

```bash
git clone https://github.com/gemechisdev/aiopyvuebot.git my-bot
cd my-bot
cp sample.env .env
# Edit .env with your values (see Environment Variables below)
```

### 2 – Install dependencies

```bash
pip install -r requirements.txt   # Python backend + bot
npm install                        # Vue.js frontend
```

### 3 – Run locally (polling mode)

```bash
# Terminal 1 – bot (polling)
python main.py

# Terminal 2 – API server (for Mini App development)
uvicorn api.index:app --reload --port 8000

# Terminal 3 – Vite dev server (hot reload)
npm run dev
```

> The Vite dev server proxies `/api/*` to `http://localhost:8000` automatically (see `vite.config.js`).

---

## 🔐 Environment Variables

Copy `sample.env` → `.env` and fill in:

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ | Telegram bot token from @BotFather |
| `MONGO_URI` | ✅ | MongoDB connection string (Atlas or self-hosted) |
| `MONGO_DB_NAME` | ❌ | Database name (default: `notebot`) |
| `WEB_APP_URL` | ✅ (prod) | Full URL of deployed Mini App for WebApp button |
| `VITE_TELEGRAM_BOT_LINK` | ✅ (prod) | `https://t.me/YourBotUsername` |
| `ADMIN_IDS` | ❌ | Comma-separated Telegram user IDs for `/stats` |
| `WEBHOOK_URL` | ❌ (prod) | App base URL – auto-registers webhook on startup |

---

## 📱 Mini App Authentication

Every `/api/notes/*` endpoint requires a valid `Authorization` header:

```
Authorization: Telegram <url-encoded Telegram initData>
```

The `telegramService.js` adds this header automatically via `window.Telegram.WebApp.initData`.  
The backend verifies the HMAC-SHA256 signature using your `BOT_TOKEN` (see `api/middleware/auth.py`).

---

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message + Open Mini App button |
| `/help` | Full command reference |
| `/addnote Title \| Content` | Save a new note |
| `/notes` | List all your notes |
| `/note <id>` | View a note in full |
| `/delnote <id>` | Delete a note |
| `/search <query>` | Full-text search |
| `/stats` | Bot stats (admin only) |
| `@bot <query>` | Search & share notes inline |

---

## 🌐 REST API

All endpoints require `Authorization: Telegram <initData>`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/notes/` | List notes (`?limit`, `?skip`, `?q`) |
| `POST` | `/api/notes/` | Create note |
| `GET` | `/api/notes/{id}` | Get single note |
| `PUT` | `/api/notes/{id}` | Update note |
| `DELETE` | `/api/notes/{id}` | Delete note |
| `POST` | `/api/notes/{id}/pin` | Toggle pin |
| `POST` | `/api/telegram/webhook` | Telegram webhook receiver |
| `GET` | `/api/telegram/setup-webhook` | Register webhook |
| `GET` | `/api/telegram/webhook-info` | Current webhook status |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/docs` | Swagger UI |

---

## 🚢 Deploy to Vercel

```bash
# 1. Push to GitHub and connect repo to Vercel
# 2. Add all environment variables in Vercel dashboard
# 3. Deploy (Vercel builds the Vue frontend and runs api/index.py as serverless function)
# 4. Register the webhook:
curl "https://your-app.vercel.app/api/telegram/setup-webhook?webhook_url=https://your-app.vercel.app"
```

---

## ➕ Adding a Plugin

Create a new file in `bot/plugins/<category>/my_feature.py`:

```python
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("mycommand"))
async def cmd_mycommand(message: Message) -> None:
    await message.reply("Hello from my plugin!")
```

Register it in `bot/__init__.py`:

```python
from bot.plugins.<category>.my_feature import router as my_router
routers = [..., my_router]
```

That's it — the router is automatically included in the Dispatcher.

---

## 📦 Tech Stack Versions

```
aiogram>=3.7.0
motor>=3.3.0
fastapi
uvicorn[standard]
pyyaml
python-dotenv

vue@^3.5
vite@^6
@tailwindcss/vite@^4
```

---

## 📄 License

MIT — fork it, build on it, ship it.

---

## 👨‍💻 Author

Built with ❤️ by [@venopyx](https://t.me/venopyx)  
Framework: [PyVueBot](https://github.com/venopyx/pyvuebot) – CLI tool for Telegram Mini Apps
