import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

def tashkeel_text(text):
    """إرسال النص لمكتبة التشكيل التلقائي"""
    try:
        url = "https://aot.me/api/v1/tashkeel"
        response = requests.post(url, json={"text": text}, timeout=10)
        if response.status_code == 200:
            return response.json().get("result", text)
    except Exception:
        pass
    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد عند تشغيل البوت"""
    await update.message.reply_text("أهلاً بك! أرسل لي أي نص عربي وسأقوم بتشكيله بالحركات الإعرابية تلقائيًا.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تشكيل النصوص التي يرسلها المستخدم أو القناة"""
    user_text = update.message.text
    if user_text:
        tashkeeled = tashkeel_text(user_text)
        await update.message.reply_text(tashkeeled)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()

