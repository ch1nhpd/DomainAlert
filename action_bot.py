import telebot
from controler import tool
import config as cf

bot = telebot.TeleBot(cf.BOT_TOKEN)

man = """
/subdomain bizflycloud.vn : echo subdomain,ip,status
/txt bizflycloud.vn : echo only subdomain
"""

def isAuthor(message, senderID=cf.AUTHOR_ID):
    return str(message.from_user.id) == senderID

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
    number_new = message.count('\n') - 1
    parts.append(f">> {number_new} domain <<")
    return parts

def alert(message,chat_id=cf.GROUP_CHAT_ID):
    with open(f"log.txt", 'w') as f:
        f.write(message)
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
        bot.reply_to(message, man)

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
        if isAuthor(message):
            a = tool(subdomain,type=0)
            content = 'done tool'
            try:
                with open(f"tmp_data/subfinder.{subdomain}.csv", 'r') as file:
                    content = file.read()
            except Exception as e:
                content += str(e)
            alert(content,1390642320)
        else:
            bot.reply_to(message, "Chưa có dữ liệu")

@bot.message_handler(commands=['txt'])
def handle_txtsubdomain(message):
    # Tách lệnh và tham số từ tin nhắn
    command, subdomain = message.text.split(maxsplit=1)
    filename = 'data_txt/'+ subdomain + '.txt'
    try:
        # Đọc nội dung từ file test.abc.com
        with open(filename, 'r') as file:
            content = file.read()
        alert(content)

    except FileNotFoundError:
        if isAuthor(message):
            a = tool(subdomain,type=0)
            content = 'done tool'
            try:
                with open(f"tmp_data/subfinder.{subdomain}.csv", 'r') as file:
                    content = file.read()
            except Exception as e:
                content += str(e)
            alert(content,1390642320)
        else:
            bot.reply_to(message, "Chưa có dữ liệu")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    sender_id = message.from_user.id
    if isAuthor(message):
        bot.reply_to(message, f"Hello")
    else:
        bot.reply_to(message, message.text)

bot.infinity_polling()