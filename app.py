from datetime import datetime
import math
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder=".")

# پایگاه داده در حافظه برای کاربران آنلاین و چت‌ها
users_db = {}
chats_db = [
    {
        "id": 1,
        "sender": "سیستم مرکزی",
        "message": (
            "به شبکه رادار و ارتباط زنده خوش آمدید. پیام‌ها برای کاربران شعاع"
            " ۱۰ کیلومتری قابل مشاهده است."
        ),
        "time": datetime.now().strftime("%H:%M"),
        "is_system": True,
    }
]


def calculate_distance(lat1, lon1, lat2, lon2):
  R = 6371.0
  dlat = math.radians(lat2 - lat1)
  dlon = math.radians(lon2 - lon1)
  a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
      math.radians(lat2)
  ) * math.sin(dlon / 2) ** 2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  return R * c


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/update-location", methods=["POST"])
def update_location():
  data = request.json
  user_id = data.get("id")
  name = data.get("name", "کاربر")
  lat = data.get("lat")
  lon = data.get("lon")

  if user_id and lat is not None and lon is not None:
    users_db[user_id] = {"id": user_id, "name": name, "lat": lat, "lon": lon}

  nearby_users = []
  current_user = users_db.get(user_id)

  if current_user:
    c_lat, c_lon = current_user["lat"], current_user["lon"]
    for uid, u_data in users_db.items():
      distance = calculate_distance(c_lat, c_lon, u_data["lat"], u_data["lon"])
      if distance <= 10.0:
        nearby_users.append(u_data)

  return jsonify({"status": "success", "nearby_users": nearby_users})


@app.route("/api/chats", methods=["GET"])
def get_chats():
  return jsonify({"status": "success", "data": chats_db})


@app.route("/api/chats", methods=["POST"])
def add_chat():
  data = request.json
  new_msg = {
      "id": len(chats_db) + 1,
      "sender_id": data.get("sender_id", "unknown"),
      "sender": data.get("sender", "کاربر"),
      "message": data.get("message", ""),
      "time": datetime.now().strftime("%H:%M"),
      "is_system": False,
  }
  chats_db.append(new_msg)
  return jsonify({"status": "success", "data": new_msg})


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)
