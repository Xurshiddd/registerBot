import telebot
import sqlite3
import pandas as pd
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7822132896:AAH7xchOGpgsO3ZWc7lP7iZCd0SB-iq7ZNY'
CHANNEL_USERNAME = '@ttysi_uz'
ADMIN_ID = 898426932  # Admin Telegram ID sini kiriting

bot = telebot.TeleBot(TOKEN)

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

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Assalomu alaykum, \"Bo'lajak yosh muhandislar\" fan olimpiadasining rasmiy telegram botiga xush kelibsiz!")
    check_subscription(message)

def check_subscription(message):
    user_status = bot.get_chat_member(CHANNEL_USERNAME, message.chat.id).status
    if user_status in ['member', 'administrator', 'creator']:
        ask_region(message)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ A'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}") )
        markup.add(InlineKeyboardButton("🔄 Tasdiqlash", callback_data='check_subscription'))
        bot.send_message(message.chat.id, "Tanlovda ishtirok etish uchun quyidagi telegram kanalga a'zo bo'lish majburiy!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'check_subscription')
def verify_subscription(call):
    user_status = bot.get_chat_member(CHANNEL_USERNAME, call.message.chat.id).status
    if user_status in ['member', 'administrator', 'creator']:
        bot.edit_message_text("✅ Siz kanalga a'zo bo'lgansiz!", call.message.chat.id, call.message.message_id)
        ask_region(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Siz hali kanalga a'zo bo'lmagansiz!")

def ask_region(message):
    markup = InlineKeyboardMarkup()
    regions = ["Toshkent", "Andijon", "Samarqand"]  # Viloyatlar ro‘yxatini to‘ldiring
    for region in regions:
        markup.add(InlineKeyboardButton(region, callback_data=f'region_{region}'))
    bot.send_message(message.chat.id, "📍 Viloyatingizni tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('region_'))
def ask_district(call):
    region = call.data.split('_')[1]
    markup = InlineKeyboardMarkup()
    districts = {"Toshkent": ["Chilonzor", "Yunusobod"], "Andijon": ["Andijon shahri"]}  # tuman.py dan olinishi kerak
    for district in districts.get(region, []):
        markup.add(InlineKeyboardButton(district, callback_data=f'district_{region}_{district}'))
    bot.edit_message_text(f"🏙 Viloyat: {region}\n📌 Tumanni tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('district_'))
def ask_institution(call):
    _, region, district = call.data.split('_')
    markup = InlineKeyboardMarkup()
    institutions = ["Maktab", "Kollej", "Texnikum", "Institut"]
    for inst in institutions:
        markup.add(InlineKeyboardButton(inst, callback_data=f'institution_{region}_{district}_{inst}'))
    bot.edit_message_text(f"🏙 Tumani: {district}\n🏫 Muassasani tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('institution_'))
def ask_name(call):
    _, region, district, institution = call.data.split('_')
    bot.send_message(call.message.chat.id, "👤 Ism va familiyangizni kiriting:")
    bot.register_next_step_handler(call.message, ask_phone, region, district, institution)

def ask_phone(message, region, district, institution):
    full_name = message.text
    bot.send_message(message.chat.id, "📞 Telefon raqamingizni kiriting:")
    bot.register_next_step_handler(message, save_data, full_name, region, district, institution)

def save_data(message, full_name, region, district, institution):
    phone = message.text
    conn = sqlite3.connect("database.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (telegram_id, full_name, phone, region, district, institution) VALUES (?, ?, ?, ?, ?, ?)",
                   (message.chat.id, full_name, phone, region, district, institution))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "✅ Ma'lumotlaringiz saqlandi!")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id == ADMIN_ID:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📥 Ma'lumotlarni yuklash", callback_data='download_data'))
        bot.send_message(message.chat.id, "📊 Admin paneliga xush kelibsiz!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'download_data')
def download_data(call):
    conn = sqlite3.connect("database.sqlite")
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    file_path = "users_data.xlsx"
    df.to_excel(file_path, index=False)
    with open(file_path, 'rb') as file:
        bot.send_document(call.message.chat.id, file)

if __name__ == '__main__':
    init_db()
    bot.polling(none_stop=True)
