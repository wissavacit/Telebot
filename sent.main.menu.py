def send_main_menu(chat_id, message_id=None, edit=False):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("📘 หลักสูตร / ค่าเทอม", url="https://bit.ly/40ezbNB"),
        InlineKeyboardButton("📅 ตารางเรียน / แผนการเรียน", url="https://regis.nsru.ac.th/apr-login/login/2")
    )
    keyboard.row(
        InlineKeyboardButton("👩‍🏫 รายชื่ออาจารย์", url="https://ms.nsru.ac.th/Personnel=3"),
        InlineKeyboardButton("🎉 กิจกรรมคณะ", url="https://ms.nsru.ac.th/Activity")
    )
    keyboard.row(
        InlineKeyboardButton("❓ FAQ", callback_data="faq_menu")
    )

    if edit and message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="📌 เลือกดูข้อมูลที่ต้องการได้เลย:",
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text="📌 เลือกดูข้อมูลที่ต้องการได้เลย:",
            reply_markup=keyboard
        )
