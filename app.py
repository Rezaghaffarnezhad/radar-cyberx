import os
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import threading

# ==================== تنظیمات ربات ====================
TOKEN = "8186173027:AAHY6oTA7TF0NWbgD_KaajJgqBZtyAu6EPc"
WEBAPP_URL = "https://rezaghaffarnezhad.github.io/radar-cyberx/"
# =======================================================

app = Flask(__name__)
active_users = {}
chat_messages = []

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/connect', methods=['POST'])
def connect_user():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'Invalid user_id'}), 400

    # ثبت یا به‌روزرسانی مشخصات کاربر
    active_users[user_id] = {
        'user_id': user_id,
        'name': data.get('name', 'کاربر تلگرام'),
        'username': data.get('username', '@user'),
        'photo_url': data.get('photo_url', ''),
        'last_seen': datetime.now()
    }

    # حذف کاربران آفلاین (بیشتر از ۳ دقیقه عدم فعالیت)
    now = datetime.now()
    expired_users = [uid for uid, u in active_users.items() if now - u['last_seen'] > timedelta(minutes=3)]
    for uid in expired_users:
        del active_users[uid]

    # ساخت لیست کاربران برای نمایش به دیگران (به جز خود کاربر)
    users_list = [
        {
            'user_id': u['user_id'],
            'name': u['name'],
            'username': u['username'],
            'photo_url': u.get('photo_url', '')
        }
        for uid, u in active_users.items() if str(uid) != str(user_id)
    ]

    return jsonify({'users': users_list})


@app.route('/api/chat', methods=['GET', 'POST'])
def chat_handler():
    global chat_messages
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        name = data.get('name', 'ناشناس')
        text = data.get('text', '').strip()
        photo_url = data.get('photo_url', '')

        if text:
            msg = {
                'id': len(chat_messages) + 1,
                'user_id': user_id,
                'name': name,
                'photo_url': photo_url,
                'text': text,
                'time': datetime.now().strftime('%H:%M')
            }
            chat_messages.append(msg)
            if len(chat_messages) > 150:
                chat_messages.pop(0)
            return jsonify({'status': 'success', 'message': msg})
        return jsonify({'error': 'Empty message'}), 400
    else:
        return jsonify({'messages': chat_messages})


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("💬 ورود به محیط چت و کاربران", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"سلام {user.first_name}! 👋\n\n"
        "به شبکه ارتباطی خوش آمدید. از طریق دکمه زیر وارد مینی‌اپلیکیشن شوید تا هم‌چت‌ها و سایر کاربران آنلاین را ببینید:",
        reply_markup=reply_markup
    )


def run_telegram_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    print("ربات تلگرام روشن شد...")
    application.run_polling()


if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.daemon = True
    bot_thread.start()

    app.run(host='0.0.0.0', port=5080, debug=False)