import pandas as pd
import subprocess
import telebot
import time

bot = telebot.TeleBot("6184106582:AAHTB8QDH1r2GMAQVIa_2pa88oJd33hWBSE")

def subfinder(domain):
    command = f"subfinder -active -all -d {domain} -ip > tmp_data/subfinder.{domain}.csv"
    # Chạy lệnh nhưng không hiển thị kết quả trực tiếp trên terminal
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Running: {command}...")
    stdout, stderr = process.communicate()
    with open(f"debug.txt", 'w') as f:
        f.write("=== STDOUT ===\n")
        f.write(stdout.decode("utf-8"))
        f.write("\n=== STDERR ===\n")
        f.write(stderr.decode("utf-8"))

    new_line = "Domain,IP,Status\n"
    with open(f"tmp_data/subfinder.{domain}.csv", 'r') as file:
        old_content = file.read()
    if not old_content.startswith("Domain,IP,Status"):   
        with open(f"tmp_data/subfinder.{domain}.csv", 'w') as file:
            file.write(new_line + old_content)

    filter(f"data/{domain}.csv",f"tmp_data/subfinder.{domain}.csv")

def tool(domain='bizflycloud.vn'): # tổng hợp từ một số tool -> chạy đa luồng, mỗi luồng một tool
    subfinder(domain)
    # subfinder -active -all -d indrive.com -ip -o subfinder.indrive.csv

def brute(): # brute force theo từ điển 
    pass

def online(): # lấy từ các web online như https://crt.sh/, https://censys.io/, https://developers.facebook.com/tools/ct/, https://www.virustotal.com/gui/domain/indrive.com/relations
    pass

def filter(oldFile='file1.csv',newFile='file2.csv'): # lọc kết quả xem có trùng với cái cũ không
# lưu vào file csv: subdomain, ip, status, dayDiscover, lastUpdate. Tên file là domain chính, 

    # Đọc hai file CSV vào DataFrame (lưu ý là 2 file phải có tên cột ở đầu)
    df1 = pd.read_csv(oldFile)
    df2 = pd.read_csv(newFile)

    # Gộp hai DataFrame lại với điều kiện cột thứ 0 là unique và chỉ giữ lại dòng cuối cùng
    merged_df = pd.concat([df1, df2]).drop_duplicates(subset=[df1.columns[0]], keep='last')

    # Lưu kết quả gộp vào file CSV
    
    # Tìm những dòng của file 2 mà giá trị cột thứ 0 không có trong cột thứ 0 của file 1
    diff_df = df2[~df2[df2.columns[0]].isin(df1[df1.columns[0]])]

    new_subdomain = '\n'.join(diff_df.apply(lambda row: f"{row[df2.columns[0]]} [{row[df2.columns[1]]}]", axis=1).values)
    merged_df.to_csv(oldFile, index=False,mode="w")
    if new_subdomain != '':
        alertNew(new_subdomain)
    
    # print(new_subdomain)
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

def alertNew(message,chat_id='-4143361119'):
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
        bot.send_message(chat_id="1390642320", text=f"Count domain = {len(domains)}")
    except Exception as e:
        pass
    for domain in domains:
        tool(domain)
    try:
        bot.send_message(chat_id="1390642320", text="End main")
    except Exception as e:
        pass
    time.sleep(3600)

while True:
    main()