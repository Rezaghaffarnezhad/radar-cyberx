import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# حافظه موقت برای نگهداری کاربران آنلاین به همراه زمان آخرین فعالیت
online_users = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>رادار سایبری - افراد آنلاین</title>
    <style>
        body { font-family: Tahoma, sans-serif; background: #f4f4f9; margin: 0; padding: 20px; }
        .counter-badge {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .pulse {
            width: 10px;
            height: 10px;
            background: #fff;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(255, 255, 255, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
        }
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background: white;
            padding: 20px;
            border-radius: 8px;
            width: 300px;
            max-height: 80vh;
            overflow-y: auto;
        }
        .close { float: left; cursor: pointer; color: red; font-weight: bold; }
    </style>
</head>
<body>

    <!-- شمارنده کاربران آنلاین در بالای صفحه -->
    <div class="counter-badge" onclick="openModal()">
        <div class="pulse"></div>
        <span>آنلاین: <span id="online-count">0</span></span>
    </div>

    <!-- مودال لیست افراد آنلاین -->
    <div id="usersModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h3>لیست افراد آنلاین</h3>
            <ul id="users-list"></ul>
        </div>
    </div>

    <script>
        const username = "کاربر_" + Math.floor(Math.random() * 1000);

        function updatePresence() {
            fetch('/api/update-presence', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username })
            });
        }

        function fetchOnlineUsers() {
            fetch('/api/online-users')
                .then(res => res.json())
                .then(users => {
                    document.getElementById('online-count').innerText = users.length;
                    const listEl = document.getElementById('users-list');
                    listEl.innerHTML = '';
                    users.forEach(user => {
                        const li = document.createElement('li');
                        li.textContent = user;
                        listEl.appendChild(li);
                    });
                });
        }

        function openModal() {
            document.getElementById('usersModal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('usersModal').style.display = 'none';
        }

        // ارسال حضور هر ۵ ثانیه یکبار
        setInterval(updatePresence, 5000);
        setInterval(fetchOnlineUsers, 5000);

        updatePresence();
        fetchOnlineUsers();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

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
    app.run(host="0.0.0.0", port=port)
