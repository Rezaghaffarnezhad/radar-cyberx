import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن ربات شما
TOKEN = "8186173027:AAHY6oTA7TF0NWbgD_KaajJgqBZtyAu6EPc"

# لینک صفحه index.html روی گیت‌هاب شما
WEB_APP_URL = "https://rezaghaffarnezhad.github.io/radar-cyberx/index.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ورود به محیط اپ", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "سلام! برای ورود به محیط برنامه روی دکمه زیر کلیک کنید:",
        reply_markup=reply_markup
    )

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
