import json
import os

def load_users(filename="users.json"):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

def broadcast_message(bot, text=None, photo_path=None, filename="users.json"):
    users = load_users(filename)
    for user_id in users:
        try:
            if photo_path and os.path.exists(photo_path):
                with open(photo_path, "rb") as photo:
                    bot.send_photo(chat_id=user_id, photo=photo, caption=text or None)
            elif text:
                bot.send_message(chat_id=user_id, text=text)
            else:
                print(f"⚠️ ไม่มีข้อมูลจะส่งไปยัง {user_id}")
            print(f"✅ ส่งข้อความไปยัง {user_id}")
        except Exception as e:
            print(f"❌ ล้มเหลวกับ {user_id}: {e}")

def broadcast_photo_bytes(bot, photo_bytes, caption=None, filename="users.json"):
    users = load_users(filename)
    for user_id in users:
        try:
            bot.send_photo(chat_id=user_id, photo=photo_bytes, caption=caption or None)
            print(f"✅ ส่งรูปให้ {user_id}")
        except Exception as e:
            print(f"❌ ล้มเหลวกับ {user_id}: {e}")
