import telebot
import os
import sqlite3
import pandas as pd
import tuman  # tuman.py dan tumanlarni olish uchun
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7822132896:AAH7xchOGpgsO3ZWc7lP7iZCd0SB-iq7ZNY'
CHANNEL_USERNAME = '@ttysi_uz'
CHANNEL_USERNAME2 = '@eduuz'
ADMIN_IDS = [629384737, 898426931]  # Bir nechta admin ID lar ro'yxati

bot = telebot.TeleBot(TOKEN)

# **Bazani yaratish**
def init_db():
    conn = sqlite3.connect("database.sqlite")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telegram_id INTEGER UNIQUE,
                        full_name TEXT,
                        phone TEXT,
                        region TEXT,
                        district TEXT,
                        institution TEXT)''')
    conn.commit()
    conn.close()

# **Userni ro‘yxatdan o‘tganligini tekshirish**
def is_registered(user_id):
    conn = sqlite3.connect("database.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# **Doimiy tugmalarni ko‘rsatish**
def send_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("Olimpiada nizomi"))
    markup.add(KeyboardButton("Hududiy mas'ullar telefon raqami"))
    markup.add(KeyboardButton("Biz bilan bog'lanish"))
    return markup
# **Start command**
@bot.message_handler(commands=['start'])
def check_subscription(message):
    if is_registered(message.chat.id):
        bot.send_message(message.chat.id, "✅ Siz allaqachon ro'yxatdan o'tgansiz!", reply_markup=send_buttons())
        return
    
    try:
        user_status = bot.get_chat_member(CHANNEL_USERNAME, message.chat.id).status
        user_stat = bot.get_chat_member(CHANNEL_USERNAME2, message.chat.id).status
        if user_status in ['member', 'administrator', 'creator'] & user_stat in ['member', 'administrator', 'creator']:
            ask_region(message)
            bot.send_message(message.chat.id, "Quyidagi menyudan tanlang:", reply_markup=send_buttons())
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("✅ A'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
            markup.add(InlineKeyboardButton("✅ A'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME2[1:]}"))
            markup.add(InlineKeyboardButton("🔄 Tasdiqlash", callback_data='check_subscription'))
            bot.send_message(message.chat.id, "Tanlovda ishtirok etish uchun quyidagi telegram kanalga a'zo bo'lish tavsiya etiladi!", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'check_subscription')
def verify_subscription(call):
    user_status = bot.get_chat_member(CHANNEL_USERNAME, call.message.chat.id).status
    user_stat = bot.get_chat_member(CHANNEL_USERNAME2, call.message.chat.id).status
    if user_status in ['member', 'administrator', 'creator'] & user_stat in ['member', 'administrator', 'creator']:
        bot.edit_message_text("✅ Siz kanalga a'zo bo'lgansiz!", call.message.chat.id, call.message.message_id)
        ask_region(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Siz hali kanalga a'zo bo'lmagansiz!")

# **Viloyatni tanlash**
def ask_region(message):
    markup = InlineKeyboardMarkup()
    for region in tuman.viloyatlar():  # tuman.py dan viloyatlar olish
        markup.add(InlineKeyboardButton(region, callback_data=f'region_{region}'))
    bot.send_message(message.chat.id, "📍 Viloyatingizni tanlang:", reply_markup=markup)

# **Tumanni tanlash**
@bot.callback_query_handler(func=lambda call: call.data.startswith('region_'))
def ask_district(call):
    region = call.data.split('_')[1]
    markup = InlineKeyboardMarkup()
    districts = tuman.get_tumanlar(region)  # tuman.py dan tumanni olish
    for district in districts:
        markup.add(InlineKeyboardButton(district, callback_data=f'district_{region}_{district}'))
    bot.edit_message_text(f"🏙 Viloyat: {region}\n📌 Tumanni tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)
# **Muassasani tanlash**
@bot.callback_query_handler(func=lambda call: call.data.startswith('district_'))
def ask_institution(call):
    _, region, district = call.data.split('_')
    markup = InlineKeyboardMarkup()
    institutions = ["Maktab", "Kollej", "Texnikum", "Institut"]
    for inst in institutions:
        markup.add(InlineKeyboardButton(inst, callback_data=f'institution_{region}_{district}_{inst}'))
    bot.edit_message_text(f"🏙 Tumani: {district}\n🏫 Muassasani tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# **Ism va familiya kiritish**
@bot.callback_query_handler(func=lambda call: call.data.startswith('institution_'))
def ask_name(call):
    _, region, district, institution = call.data.split('_')
    bot.send_message(call.message.chat.id, "👤 Ism va familiyangizni kiriting:")
    bot.register_next_step_handler(call.message, ask_phone, region, district, institution)

# **Telefon raqamini kiritish**
def ask_phone(message, region, district, institution):
    full_name = message.text
    bot.send_message(message.chat.id, "📞 Telefon raqamingizni kiriting:")
    bot.register_next_step_handler(message, save_data, full_name, region, district, institution)

# **Ma'lumotlarni saqlash**
def save_data(message, full_name, region, district, institution):
    phone = message.text
    conn = sqlite3.connect("database.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (telegram_id, full_name, phone, region, district, institution) VALUES (?, ?, ?, ?, ?, ?)",
                   (message.chat.id, full_name, phone, region, district, institution))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "✅ Ma'lumotlaringiz saqlandi! \n Olimpiadaning birinchi bosqichi 8-aprel kuni soat 10:00 da bo'lib o'tadi. \nQo'shimcha savollar yuzasidan hududiy mas'ullar bilan bog'lanishingiz mumkin.")

# **Admin panel**
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id in ADMIN_IDS:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📥 Ma'lumotlarni yuklash", callback_data='download_data'))
        bot.send_message(message.chat.id, "📊 Admin paneliga xush kelibsiz!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'download_data')
def download_data(call):
    if call.message.chat.id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ Siz admin emassiz!")
        return

    conn = sqlite3.connect("database.sqlite")
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    
    file_path = "users_data.xlsx"
    df.to_excel(file_path, index=False)

    with open(file_path, 'rb') as file:
        bot.send_document(call.message.chat.id, file)
    os.remove(file_path)

# **Tugmalarga tegishli handlerlar**
@bot.message_handler(func=lambda message: message.text == "Olimpiada nizomi")
def send_regulations(message):
    with open("nizom.pdf", 'rb') as file:
        bot.send_document(message.chat.id, file)



contacts = {
    "Qoraqalpog‘iston Respublikasi": "Mavlyanov Aybek Palvanbayevich - ishchi guruh rahbari, Kafedra mudiri\n☎ 88-008-82-01",
    "Andijon viloyati": "Axmedov Jaxongir Adxamovich - ishchi guruh rahbari, Professor\n☎ 93-591-44-22",
    "Buxoro viloyati": "Arabov Jamoliddin Sadriddinovich - ishchi guruh rahbari, Kafedra mudiri\n☎ 97-441-41-71",
    "Jizzax viloyati": "Xazratkulov Xamidjon Alikulovich - ishchi guruh rahbari, Bo‘lim boshlig‘i\n☎ 90-357-06-65",
    "Qashqadaryo viloyati": "Mansurov Mansur Alisherovich - ishchi guruh rahbari, Dekan\n☎ 98-128-33-28",
    "Navoiy viloyati": "Eshnazarov Dilshod Azamatovich - ishchi guruh rahbari, Assistent\n☎ 94-627-25-93",
    "Namangan viloyati": "Kadirov Oman Xamidovich - ishchi guruh rahbari, Kafedra mudiri\n☎ 99-307-77-63",
    "Samarqand viloyati": "Ulukmuradov Abror Nafasovich - ishchi guruh rahbari, Kafedra mudiri\n☎ 97-490-30-72, 98-001-14-72",
    "Surxondaryo viloyati": "Rasulov Hamza Yuldoshevich - ishchi guruh rahbari, Dotsent\n☎ 90-988-79-63",
    "Sirdaryo viloyati": "Davlyatov Bekzodjon Aslanxojayevich - ishchi guruh rahbari, Kafedra mudiri\n☎ 94-656-82-01",
    "Toshkent viloyati>": "Ortiqov Oybek Akbaraliyevich - ishchi guruh rahbari, Kafedra mudiri\n☎ 90-806-59-37",
    "Farg‘ona viloyati": "Tuychiyev Timur Ortikovich - ishchi guruh rahbari, Dotsent\n☎ 97-747-34-06",
    "Xorazm viloyati": "Ruzmetov Mansurbek Erkinovich - ishchi guruh rahbari, Dekan\n☎ 90-984-20-18",
    "Toshkent shahri": "Patxullayev Sarvarjon Ubaydulla o‘g‘li - ishchi guruh rahbari, Dekan\n☎ 90-325-06-06"
}

@bot.message_handler(func=lambda message: message.text == "Hududiy mas'ullar telefon raqami")
def send_regions(message):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=region, callback_data=region) for region in contacts]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Viloyatni tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in contacts)
def send_contact(call):
    contact_info = f"📍 <b>{call.data}</b>\n{contacts[call.data]}"
    bot.send_message(call.message.chat.id, contact_info, parse_mode="HTML")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: message.text == "Biz bilan bog'lanish")
def send_contact_number(message):
    bot.send_message(message.chat.id, "📞 +998555127000")

if __name__ == '__main__':
    init_db()
    bot.polling(none_stop=True)