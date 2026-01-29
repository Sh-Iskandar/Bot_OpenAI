import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from openai import OpenAI

OPENAI_KEY = os.environ["OPENAI_KEY"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

client = OpenAI(api_key=OPENAI_KEY)

app = Application.builder().token(BOT_TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": text}]
    )

    await update.message.reply_text(response.choices[0].message.content)

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def handler(request):
    await app.initialize()
    await app.process_update(Update.de_json(await request.json(), app.bot))
    return {"status": "ok"}