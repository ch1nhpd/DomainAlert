import telebot

bot = telebot.TeleBot("6184106582:AAHTB8QDH1r2GMAQVIa_2pa88oJd33hWBSE")

def split_long_message(message, max_length):
    """
    Chia tin nhắn thành các phần có độ dài tối đa và giữ nguyên các dòng
    """
    parts = []
    current_part = ""

    for line in message.split('\n'):
        if len(current_part) + len(line) + 1 <= max_length:  # Kiểm tra độ dài của phần hiện tại và dòng mới
            if current_part:  # Kiểm tra xem phần hiện tại có rỗng không
                current_part += '\n'  # Thêm dấu xuống dòng nếu phần hiện tại không rỗng
            current_part += line  # Thêm dòng vào phần hiện tại
        else:
            parts.append(current_part)  # Lưu phần hiện tại vào danh sách các phần
            current_part = line  # Bắt đầu một phần mới

    parts.append(current_part)  # Lưu phần cuối cùng vào danh sách các phần
    number_new = message.count('\n') + 1
    parts.append(f">> {number_new} domain <<")
    return parts

def alert(message,chat_id='-4069733583'):
    max_length = 4096
    message_parts = split_long_message(message, max_length)
    for part in message_parts:
        try:
        # Lệnh gửi tin nhắn
            bot.send_message(chat_id=chat_id, text=part)
        except Exception as e:
            bot.send_message(chat_id=chat_id, text=e)
  

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['subdomain'])
def handle_subdomain(message):
    # Tách lệnh và tham số từ tin nhắn
    command, subdomain = message.text.split(maxsplit=1)
    filename = 'data/'+ subdomain + '.csv'
    try:
        # Đọc nội dung từ file test.abc.com
        with open(filename, 'r') as file:
            content = file.read()
        alert(content)

    except FileNotFoundError:
        bot.reply_to(message, "Chưa có dữ liệu")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
        bot.reply_to(message, message.text)

bot.infinity_polling()