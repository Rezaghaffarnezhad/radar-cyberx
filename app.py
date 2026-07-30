import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# حافظه موقت برای ذخیره‌سازی داده‌های مینی‌اپ
users_db = {}
messages_db = []
system_logs = []

@app.route('/')
def index():
    return render_template('index.html')

# مدیریت پروفایل و تنظیمات کاربری
@app.route('/api/profile', methods=['GET', 'POST'])
def manage_profile():
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        
        users_db[user_id] = {
            "name": data.get('name', 'Anonymous Cyber Agent'),
            "bio": data.get('bio', 'در حال بررسی سیگنال‌ها...'),
            "avatar_color": data.get('avatar_color', '#00ffcc'),
            "ghost_mode": data.get('ghost_mode', False),
            "radar_radius": data.get('radar_radius', 5.0),
            "social_link": data.get('social_link', ''),
            "badges": data.get('badges', ['پیشگام رادار']),
            "saved_places": data.get('saved_places', []),
            "theme": data.get('theme', 'cyberpunk'),
            "activity_stats": {
                "online_time_mins": data.get('online_time_mins', 15),
                "messages_sent": data.get('messages_sent', 0)
            }
        }
        return jsonify({"status": "success", "profile": users_db[user_id]})
    
    user_id = request.args.get('user_id')
    profile = users_db.get(user_id, {
        "name": "کاربر جدید", 
        "ghost_mode": False, 
        "radar_radius": 5.0,
        "bio": "آماده برای اسکن محیط"
    })
    return jsonify({"status": "success", "profile": profile})

# هسته رادار و اسکن محیط
@app.route('/api/radar/scan', methods=['POST'])
def radar_scan():
    data = request.json
    user_id = data.get('user_id')
    lat = data.get('lat')
    lng = data.get('lng')
    frequency_band = data.get('frequency_band', '5km')
    is_cloaked = data.get('is_cloaked', False)
    
    if user_id not in users_db:
        users_db[user_id] = {
            "name": f"عامل_{user_id[-4:]}", 
            "ghost_mode": is_cloaked,
            "cloaked": is_cloaked
        }
    
    users_db[user_id]['location'] = {"lat": lat, "lng": lng}
    users_db[user_id]['cloaked'] = is_cloaked
    
    detected_targets = []
    for uid, udata in users_db.items():
        if uid == user_id or udata.get('ghost_mode') or udata.get('cloaked'):
            continue
        if 'location' in udata:
            detected_targets.append({
                "user_id": uid,
                "name": udata.get('name'),
                "bio": udata.get('bio'),
                "avatar_color": udata.get('avatar_color', '#00ffcc'),
                "location": udata['location'],
                "distance_km": 1.2
            })
            
    system_logs.append(f"اسکن روی باند {frequency_band} توسط کاربر {user_id} انجام شد.")
    
    return jsonify({
        "status": "success",
        "frequency_band": frequency_band,
        "targets": detected_targets,
        "system_status": "SECURE"
    })

# سیستم چت (عمومی و خصوصی)
@app.route('/api/chat', methods=['GET', 'POST'])
def handle_chat():
    if request.method == 'POST':
        data = request.json
        msg_type = data.get('type', 'public')
        sender = data.get('sender')
        receiver = data.get('receiver', None)
        text = data.get('text')
        
        message = {
            "sender": sender,
            "receiver": receiver if msg_type == 'dm' else None,
            "type": msg_type,
            "text": text,
            "timestamp": "2026-07-30T13:00:00Z"
        }
        messages_db.append(message)
        
        if sender in users_db and "activity_stats" in users_db[sender]:
            users_db[sender]["activity_stats"]["messages_sent"] += 1
            
        return jsonify({"status": "success", "message": message})
        
    chat_type = request.args.get('type', 'public')
    user_id = request.args.get('user_id')
    
    if chat_type == 'dm':
        filtered_msgs = [m for m in messages_db if m['type'] == 'dm' and (m['sender'] == user_id or m['receiver'] == user_id)]
    else:
        filtered_msgs = [m for m in messages_db if m['type'] == 'public']
        
    return jsonify({"status": "success", "messages": filtered_msgs})

# تنظیمات کلی سیستم
@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        data = request.json
        return jsonify({"status": "success", "settings": data})
    return jsonify({
        "status": "success",
        "available_languages": ["fa", "en"],
        "default_data_saver": False,
        "haptics_enabled": True,
        "app_version": "1.0.0-cyberx"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
