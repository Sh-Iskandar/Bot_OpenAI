# api/bot.py
import os
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import openai

# Создаём Flask приложение для Vercel
app = Flask(__name__)

# Получаем токены из Environment Variables
BOT_TOKEN = os.environ["BOT_TOKEN"]
OPENAI_KEY = os.environ["OPENAI_KEY"]

# Настройка OpenAI
client = openai.OpenAI(api_key=OPENAI_KEY)

# Создаём Telegram приложение
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask endpoint для Vercel
@app.route("/api/bot", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)
    return jsonify({"ok": True})
