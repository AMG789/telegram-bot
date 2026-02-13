import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread
import google.generativeai as genai

# ================== Environment Variables ==================
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ================== Configure Gemini ==================
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ================== Flask ==================
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت الذكي يعمل!"

def run_flask():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

# ================== Commands ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 مرحباً! أنا بوت ذكاء اصطناعي مجاني 100٪\n\n"
        "الأوامر:\n"
        "/ask سؤالك\n"
        "/help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "استخدم:\n"
        "/ask ثم سؤالك\n\n"
        "أو اكتب أي رسالة مباشرة."
    )

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = ' '.join(context.args)

    if not user_question:
        await update.message.reply_text("❌ اكتب سؤالك بعد /ask")
        return

    await update.message.chat.send_action(action="typing")

    try:
        response = model.generate_content(user_question)
        await update.message.reply_text(f"🤖 {response.text}")

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    await update.message.chat.send_action(action="typing")

    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(f"🤖 {response.text}")

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

# ================== Main ==================
def main():
    Thread(target=run_flask, daemon=True).start()

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ask", ask))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 البوت يعمل الآن...")
    application.run_polling()

if __name__ == "__main__":
    main()
