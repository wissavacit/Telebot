from config import API_TOKEN
import telebot
import os
import json
from broadcast import broadcast_message, broadcast_photo_bytes
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot(token=API_TOKEN)

def save_user_id(user_id):
    file_path = "users.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        users = json.load(f)

    if user_id not in users:
        users.append(user_id)
        with open(file_path, "w") as f:
            json.dump(users, f, indent=4)
        print(f"✅ เพิ่ม user ใหม่: {user_id}")
    else:
        print(f"ℹ️ user เดิม: {user_id}")

def send_main_menu(bot, chat_id, message_id=None, edit=False):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("📘 หลักสูตร / ค่าเทอม", url="https://bit.ly/40ezbNB"),
        InlineKeyboardButton("📅 ตารางเรียน / แผนการเรียน", url="https://regis.nsru.ac.th/apr-login/login/2")
    )
    keyboard.row(
        InlineKeyboardButton("👩‍🏫 รายชื่ออาจารย์", url="https://ms.nsru.ac.th/Personnel=3"),
        InlineKeyboardButton("🎉 กิจกรรมคณะ", url="https://ms.nsru.ac.th/Activity"),
        InlineKeyboardButton("🗺️  แผนที่", callback_data="faq_map")
    )
    keyboard.row(
        InlineKeyboardButton("📝ช่องทางติดตามข่าวสารและบริการนักศึกษา",callback_data="faq_list")
    )
    keyboard.row(
        InlineKeyboardButton("❓ FAQ", callback_data="faq_menu")
    )
    
    text = "📌 เลือกดูข้อมูลที่ต้องการได้เลย:"
    if edit and message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)

    
@bot.message_handler(commands=['start']) 
def welcome(message):
    user_id = message.chat.id
    save_user_id(user_id)

    welcome_text = f'สวัสดี {message.from_user.first_name} วันนี้ให้ฉันช่วยอะไรดี?'
    bot.send_message(chat_id=user_id, text=welcome_text)
    send_main_menu(bot, chat_id=user_id)

@bot.message_handler(commands=['broadcast'])
def handle_broadcast(message):
    admin_id = 6448266873  
    if message.chat.id != admin_id:
        bot.reply_to(message, "❌ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้")
        return

    content = message.text[len("/broadcast "):].strip()
    if '|' in content:
        photo_path, text = content.split('|', 1)
        photo_path = photo_path.strip()
        text = text.strip()
        broadcast_message(bot, text=text, photo_path=photo_path)
    else:
        broadcast_message(bot, text=content)

    bot.reply_to(message, "✅ ส่งข่าวสารเรียบร้อยแล้ว!")

@bot.message_handler(content_types=['photo'])
def handle_photo_broadcast(message):
    admin_id = 6448266873  
    if message.chat.id != admin_id:
        bot.reply_to(message, "❌ คุณไม่มีสิทธิ์ส่งภาพ broadcast")
        return

    print("📸 ได้รับภาพจาก admin")

    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    photo_data = bot.download_file(file_info.file_path)

    print("📤 เริ่ม broadcast ภาพ...")

    broadcast_photo_bytes(bot, photo_bytes=photo_data, caption=message.caption or None)

    bot.reply_to(message, "✅ ส่งภาพ broadcast เรียบร้อยแล้ว!")

@bot.callback_query_handler(func=lambda call: call.data == "faq_list")
def faq_list(call):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🏛️ เพจมหาวิทยาลัย", url="https://www.facebook.com/nsrunews"))
    keyboard.add(InlineKeyboardButton("💰 เพจ กองทุนกู้ยืม (กยศ.)", url="https://www.facebook.com/profile.php?id=100069385112013"))
    keyboard.add(InlineKeyboardButton("🗂️ เพจ สำนักส่งเสริมวิชาการและงานทะเบียน", url="https://www.facebook.com/aprnsru"))
    keyboard.add(InlineKeyboardButton("🎓 เพจ กองพัฒนานักศึกษา", url="https://www.facebook.com/studentnsru"))
    keyboard.add(InlineKeyboardButton("👥 เพจ องค์การบริหารนักศึกษาฯ", url="https://www.facebook.com/orgnsrupage"))
    keyboard.add(InlineKeyboardButton("🎯 เพจ งานแนะแนวและทุนการศึกษา", url="https://www.facebook.com/profile.php?id=100064650644030"))
    keyboard.add(InlineKeyboardButton("🔙 ย้อนกลับ", callback_data="back_to_main"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📖 กรุณาเลือกหัวข้อที่ต้องการ:",
        reply_markup=keyboard
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "faq_menu")
def faq_menu(call):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📄 การยื่นเอกสารขอจบ", callback_data="faq_graduate_docs"))
    keyboard.add(InlineKeyboardButton("🧑‍🏫 การติดต่ออาจารย์", callback_data="faq_contact_teacher"))
    keyboard.add(InlineKeyboardButton("📊 เกรดเฉลี่ยขั้นต่ำในการจบ", callback_data="faq_gpa_required"))
    keyboard.add(InlineKeyboardButton("📝 ปัญหาการลงทะเบียนเรียน", callback_data="faq_registration_issue"))
    keyboard.add(InlineKeyboardButton("🔙 ย้อนกลับ", callback_data="back_to_main"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📖 คำถามที่พบบ่อย\nกรุณาเลือกหัวข้อที่ต้องการ:",
        reply_markup=keyboard
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main(call):
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    except Exception as e:
        print(f"⚠️ ลบข้อความไม่ได้: {e}")

    send_main_menu(bot, chat_id=call.message.chat.id)
    bot.answer_callback_query(call.id)



@bot.callback_query_handler(func=lambda call: call.data.startswith("faq_") and call.data not in ["faq_menu", "faq_map"])
def answer_faq(call):
    answers = {
        "faq_graduate_docs": "📄 การยื่นเอกสารขอจบ:\nนักศึกษาตรวจสอบเอกสารที่ต้องใช้ได้ที่เว็บไซต์ของคณะ หรือติดต่อฝ่ายทะเบียน\nแนะนำให้ยื่นล่วงหน้าก่อนหมดเขตตามปฏิทินการศึกษา",
        "faq_contact_teacher": "🧑‍🏫 การติดต่ออาจารย์:\nตรวจสอบรายชื่อและช่องทางติดต่อที่: https://ms.nsru.ac.th/Personnel=3\nหรือติดต่อในวันให้คำปรึกษาตามรายวิชาที่เรียน",
        "faq_gpa_required": "📊 เกรดเฉลี่ยขั้นต่ำในการจบ:\nต้องมี GPA รวมไม่ต่ำกว่า 2.00 และไม่มีวิชาติด I, W หรือ F ที่ยังไม่สะสาง",
        "faq_registration_issue": "📝 ปัญหาการลงทะเบียนเรียน:\nติดต่อเจ้าหน้าที่คณะ หรือฝ่ายทะเบียนโดยเร็วหากพบปัญหาในการลงทะเบียน"
    }

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 กลับไปเมนู FAQ", callback_data="faq_menu"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=answers.get(call.data, "❌ ไม่มีข้อมูลคำตอบ"),
        reply_markup=keyboard
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == "faq_map")
def send_map(call):
    bot.answer_callback_query(call.id)

    with open("C:/Users/pview/OneDrive/Desktop/map.jpg", "rb") as photo:
        media = InputMediaPhoto(photo, caption="🗺️ แผนที่มหาวิทยาลัย\n\nสามารถดูตำแหน่งอาคารต่าง ๆ ได้จากภาพนี้")

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🔙 ย้อนกลับ", callback_data="back_to_main"))

        bot.edit_message_media(
            media=media,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )

bot.polling()
