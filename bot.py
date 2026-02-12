import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread
import google.generativeai as genai

# التوكنات من Railway
TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_ai(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "messages": [
                {"role": "user", "content": prompt}
            ],
        },
    )

    return response.json()["choices"][0]["message"]["content"]

# إعداد



# Flask للحفاظ على استيقاظ البوت
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت الذكي يعمل!"

def run_flask():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

# ========== أوامر البوت ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 مرحباً! أنا بوت ذكي باستخدام AMG"
        "الأوامر المتاحة:\n"
        "/start - بدء البوت\n"
        "/ask [سؤالك] - اسألني أي شيء\n"
        "/help - المساعدة"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 كيفية الاستخدام:\n\n"
        "1. /ask ثم اكتب سؤالك\n"
        "   مثال: /ask ما هو أفضل كتاب في البرمجة؟\n\n"
        "2. أو اكتب أي شيء مباشرة وسأرد عليك!"
    )

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = ' '.join(context.args)
    
    if not user_question:
        await update.message.reply_text("❌ اكتب سؤالك بعد /ask\nمثال: /ask ما هو الذكاء الاصطناعي؟")
        return
    
    # إظهار "جاري الكتابة..."
    await update.message.chat.send_action(action="typing")
    
    try:
        # إرسال السؤال لـ Gemini
    reply = ask_ai(user_text)
await update.message.reply_text(reply)
         
    
        
        await update.message.reply_text(f"🤖 {answer}")
        
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # الرد على أي رسالة عادية
    user_message = update.message.text
    
    # إظهار "جاري الكتابة..."
    await update.message.chat.send_action(action="typing")
    
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(f"🤖 {response.text}")
        
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

def main():
    # تشغيل Flask
    Thread(target=run_flask, daemon=True).start()
    
    # إعداد البوت
    application = Application.builder().token(TOKEN).build()
    
    # الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ask", ask))
    
    # الرد على الرسائل العادية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 البوت الذكي يعمل الآن...")
    application.run_polling()

if __name__ == "__main__":
    main()
