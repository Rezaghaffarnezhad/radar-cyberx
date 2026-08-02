import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن ربات خود را از BotFather بگیرید
TOKEN = "8186173027:AAHY6oTA7TF0NWbgD_KaajJgqBZtyAu6EPc"

# لینک اینترنتی فایل index.html که روی گیت‌هاب یا هاست آپلود کرده‌اید را اینجا قرار دهید
WEB_APP_URL = "https://your-username.github.io/your-repo/index.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ساخت دکمه شیشه‌ای ورود به اپلیکیشن
    keyboard = [
        [InlineKeyboardButton("ورود به اپلیکیشن", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ارسال پیام خوش‌آمدگویی و نمایش دکمه
    await update.message.reply_text(
        "سلام! برای ورود به نقشه و چت آنلاین روی دکمه زیر کلیک کنید:",
        reply_markup=reply_markup
    )

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    # ثبت دستور start
    application.add_handler(CommandHandler("start", start))
    
    # اجرای ربات
    application.run_polling()

if __name__ == "__main__":
    main()
