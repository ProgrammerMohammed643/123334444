import telebot
from datetime import datetime
import threading
import time
import pytz

bot = telebot.TeleBot('7498694042:AAHfDRfVZq8p3zC0Bfc6pnyRi_-rF13-lgw')  
GROUP_ID = None
user_id = None  

def update_group_bio(chat_id, timezone):
    while True:
        current_time = datetime.now(timezone).strftime("%Y-%m-%d %I:%M %p")
        new_description = f"صلي على النبي وتبسم ♥️✨\n\n{current_time}"  


        try:
            chat_info = bot.get_chat(chat_id)
            current_description = chat_info.description
        except Exception as e:
            print(f"Error fetching chat description: {e}")
            return


        if new_description != current_description:
            try:
                bot.set_chat_description(chat_id, new_description)
                print(f"Updated chat description to: {new_description}")
            except Exception as e:
                print(f"Error updating chat description: {e}")

        time.sleep(60)  # الانتظار لمدة دقيقة قبل التحديث التالي

def get_timezone(country):
    if country == 'مصر':
        return pytz.timezone('Africa/Cairo')
    elif country == 'العراق':
        return pytz.timezone('Asia/Baghdad')
    elif country == 'سوريا':
        return pytz.timezone('Asia/Damascus')
    elif country == 'لبنان':
        return pytz.timezone('Asia/Beirut')
    return None

@bot.message_handler(commands=['time'])
def handle_start(message):
    global user_id, GROUP_ID
    user_id = message.from_user.id  
    GROUP_ID = message.chat.id

    keyboard = telebot.types.InlineKeyboardMarkup()
    countries = ['مصر', 'العراق', 'سوريا', 'لبنان']
    for country in countries:
        keyboard.add(telebot.types.InlineKeyboardButton(text=country, callback_data=country))
    

    bot.send_message(message.chat.id, "اختر دولة للحصول على التوقيت:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_country_selection(call):
    global GROUP_ID, user_id
    timezone = get_timezone(call.data)
    
    if timezone:

        bot.reply_to(call.message, f"تم بدء التحديث بتوقيت {call.data}.")
        threading.Thread(target=update_group_bio, args=(GROUP_ID, timezone)).start()
        

        bot.send_message(user_id, f"تم بدء التحديث بتوقيت {call.data}.")
    else:
        bot.reply_to(call.message, "حدث خطأ أثناء تحديد المنطقة الزمنية.")

bot.polling()  
