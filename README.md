# 🔒 WhispierBot

A modern Telegram bot for sending secret whisper messages that only specific people can read, even in public groups!

![WhispierBot](https://img.shields.io/badge/WhispierBot-1.0.0-purple?style=for-the-badge&logo=telegram)

## ✨ Features

- 🔐 **Secret Messages**: Send whispers that only specific users can read
- 👥 **Group Compatible**: Works in any chat or group, even if the bot isn't there
- 🚀 **Fast & Reliable**: Built on modern serverless architecture
- ⏰ **Auto-Expires**: Messages automatically expire after 7 days for security
- 🆓 **Free**: Completely free to use
- 🛡️ **Secure**: Messages are securely stored and encrypted

## 🚀 How to Use

1. **Start the bot**: Send `/start` to [@whispierbot](https://t.me/whispierbot)
2. **Create a whisper**: Type `@whispierbot` in any chat
3. **Write your message**: Add your secret message
4. **Add recipient**: End with the recipient's @username or ID
5. **Send**: Only the recipient can open and read the message!

### Example
```
@whispierbot This is a secret message @username
```

## 🏗️ Tech Stack

- **Backend**: FastAPI with Python
- **Database**: Supabase PostgreSQL
- **Frontend**: Vue.js 3 with Tailwind CSS v4
- **Deployment**: Vercel Serverless Functions
- **Bot API**: python-telegram-bot library
- **Architecture**: PyVueBot framework

## 🔧 Development Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Supabase account
- Telegram Bot Token

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/venopyx/whispierbot.git
cd whispierbot
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your actual values
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Node.js dependencies**
```bash
npm install
```

5. **Set up Supabase database**
   - Create a new Supabase project
   - Run the SQL commands from `api/db.py` in the SQL editor
   - Get your project URL and anon key

6. **Configure Telegram bot**
   - Create a bot with [@BotFather](https://t.me/BotFather)
   - Enable inline mode in bot settings
   - Set inline feedback to 100%
   - Get your bot token

### Local Development

1. **Start the frontend**
```bash
npm run dev
```

2. **Start the backend** (in another terminal)
```bash
uvicorn api.index:app --reload --port 8000
```

3. **Set up webhook** (for testing)
```bash
curl -X GET "http://localhost:8000/api/telegram/setup-webhook?webhook_url=https://your-ngrok-url.com/api/telegram/webhook"
```

## 🚀 Deployment

### Deploy to Vercel

1. **Connect your repository to Vercel**
2. **Add environment variables in Vercel dashboard**
3. **Deploy**: Vercel will automatically build and deploy
4. **Set webhook**: Visit `https://your-app.vercel.app/api/telegram/setup-webhook?webhook_url=https://your-app.vercel.app/api/telegram/webhook`

### Environment Variables

Required environment variables:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
ADMIN_USER_ID=your_telegram_user_id  # Optional
NODE_ENV=production
```

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  target_user JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Whispers Table
```sql
CREATE TABLE whispers (
  inline_message_id VARCHAR PRIMARY KEY,
  message TEXT NOT NULL,
  sender_id BIGINT REFERENCES users(id),
  recipient_ids BIGINT[] NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days')
);
```

## 🛠️ API Endpoints

- `POST /api/telegram/webhook` - Handle Telegram updates
- `GET /api/telegram/setup-webhook` - Set up webhook URL
- `GET /api/health` - Health check endpoint
- `GET /api/docs` - API documentation

## 📝 Commands

- `/start` - Welcome message and instructions
- `/help` - How to use the bot
- `/stats` - Statistics (admin only)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

Built with ❤️ by [@venopyx](https://t.me/venopyx)

**Framework**: [PyVueBot](https://github.com/venopyx/pyvuebot) - Modern CLI tool for Telegram Mini Apps

## 🔗 Links

- **Bot**: [@whispierbot](https://t.me/whispierbot)
- **Developer**: [@venopyx](https://t.me/venopyx)
- **Framework**: [PyVueBot](https://github.com/venopyx/pyvuebot)

---

⭐ **Star this repository if you find it useful!**