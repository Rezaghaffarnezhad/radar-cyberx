import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن ربات شما
TOKEN = "8186173027:AAHY6oTA7TF0NWbgD_KaajJgqBZtyAu6EPc"

# لینک صفحه index.html روی گیت‌هاب شما
WEB_APP_URL = "https://rezaghaffarnezhad.github.io/radar-cyberx/index.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    
    # دکمه‌های جذاب‌تر و حرفه‌ای‌تر
    keyboard = [
        [InlineKeyboardButton("🚀 ورود به محیط اپلیکیشن", web_app=WebAppInfo(url=WEB_APP_URL))],
        [
            InlineKeyboardButton("📖 راهنما", callback_data="help"),
            InlineKeyboardButton("💬 پشتیبانی", url="https://t.me/Rezaghaffarnezhad")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # پیام خوش‌آمدگویی شخصی‌سازی‌شده
    await update.message.reply_text(
        f"سلام {user_name} عزیز! 🌟\nبه ربات نقشه و چت زنده خوش آمدید.\n\nبرای ورود به محیط برنامه روی دکمه زیر کلیک کنید:",
        reply_markup=reply_markup
    )

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
