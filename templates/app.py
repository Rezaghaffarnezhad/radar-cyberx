import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# حافظه موقت برای نگهداری کاربران آنلاین
online_users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/update-presence', methods=['POST'])
def update_presence():
    data = request.get_json()
    username = data.get('username')
    if username:
        online_users[username] = True
    return jsonify({"status": "success"})

@app.route('/api/online-users', methods=['GET'])
def get_online_users():
    return jsonify(list(online_users.keys()))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
