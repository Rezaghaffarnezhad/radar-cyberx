import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# یک حافظه موقت (مجموعه) برای نگهداری نام یا آیدی کاربران آنلاین
# (در صورت نیاز می‌توانید بعدها این را به دیتابیس متصل کنید)
online_users_set = set()

@app.route('/')
def index():
    # صفحه اصلی نقشه/چت
    return render_template('index.html')

@app.route('/api/update-presence', methods=['POST'])
def update_presence():
    """کاربر وقتی وارد سایت می‌شود، حضور خود را اعلام می‌کند"""
    data = request.get_json()
    username = data.get('username')
    if username:
        online_users_set.add(username)
    return jsonify({"status": "success"})

@app.route('/api/online-users', methods=['GET'])
def get_online_users():
    """لیست افراد آنلاین را به فرانت‌اند بر می‌گرداند"""
    return jsonify(list(online_users_set))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
