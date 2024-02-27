import pandas as pd
import subprocess
import telebot
import time
import config as cf
from controler import tool

bot = telebot.TeleBot(cf.BOT_TOKEN)

def brute(): # brute force theo từ điển 
    pass

def online(): # lấy từ các web online như https://crt.sh/, https://censys.io/, https://developers.facebook.com/tools/ct/, https://www.virustotal.com/gui/domain/indrive.com/relations
    pass

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

def alertNew(message,chat_id=cf.GROUP_CHAT_ID):
    max_length = 4096
    message_parts = split_long_message(message, max_length)
    for part in message_parts:
        try:
        # Lệnh gửi tin nhắn
            bot.send_message(chat_id=chat_id, text=part)
        except Exception as e:
            bot.send_message(chat_id=chat_id, text=e)
    

def alertSub():
    pass

def checkStatus():
    # update cả status của những cái cũ (trước mắt là update những cái die, lập lịch để check)
    pass

def main():
    with open(f"listdomain.txt", 'r') as file:
        listdomain = file.read()
    domains = listdomain.split('\n')
    try:
        bot.send_message(chat_id=cf.AUTHOR_ID, text=f"Count domain = {len(domains)}")
    except Exception as e:
        pass

    for domain in domains:
        new_subdomain = tool(domain)
        if new_subdomain != '' and new_subdomain != 0:
            alertNew(new_subdomain)

    try:
        bot.send_message(chat_id=cf.AUTHOR_ID, text="End main")
    except Exception as e:
        pass
    time.sleep(cf.TIME_SLEEP)

while True:
    main()