import telebot

bot = telebot.TeleBot("6184106582:AAHTB8QDH1r2GMAQVIa_2pa88oJd33hWBSE")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['subdomain'])
def handle_subdomain(message):
    # Tách lệnh và tham số từ tin nhắn
    command, subdomain = message.text.split(maxsplit=1)
    filename = subdomain + '.csv'
    try:
        # Đọc nội dung từ file test.abc.com
        with open(filename, 'r') as file:
            content = file.read()
        bot.reply_to(message, content)
    except FileNotFoundError:
        bot.reply_to(message, "Chưa có dữ liệu")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
        bot.reply_to(message, message.text)

# bot.infinity_polling()