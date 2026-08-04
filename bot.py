import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# خواندن توکن به صورت امن از متغیرهای محیطی هاست
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# لینک صفحه index.html روی گیت‌هاب شما
WEB_APP_URL = "https://rezaghaffarnezhad.github.io/radar-cyberx/index.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    
    keyboard = [
        [InlineKeyboardButton("🚀 ورود به محیط اپلیکیشن", web_app=WebAppInfo(url=WEB_APP_URL))],
        [
            InlineKeyboardButton("📖 راهنما", callback_data="help"),
            InlineKeyboardButton("💬 پشتیبانی", url="https://t.me/Rezaghaffarnezhad")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"سلام {user_name} عزیز! 🌟\nبه ربات نقشه و چت زنده خوش آمدید.\n\nبرای ورود به محیط برنامه روی دکمه زیر کلیک کنید:",
        reply_markup=reply_markup
    )

def main():
    if not TOKEN:
        raise ValueError("توکن ربات تلگرام (TELEGRAM_BOT_TOKEN) تنظیم نشده است!")
        
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
