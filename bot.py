import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

# التوكن من Railway (مش هنحطه هنا)
TOKEN = os.getenv("BOT_TOKEN")

# Flask للحفاظ على استيقاظ البوت
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت يعمل!"

def run_flask():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 البوت يعمل على الاستضافة 24/7!")

def main():
    # تشغيل Flask في خيط منفصل
    Thread(target=run_flask, daemon=True).start()
    
    # تشغيل البوت
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("🚀 البوت يعمل الآن...")
    application.run_polling()

if __name__ == "__main__":
    main()
