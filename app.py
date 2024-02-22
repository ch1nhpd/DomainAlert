import pandas as pd
import subprocess
import echo_bot

def subfinder(domain):
    command = f"subfinder -active -all -d {domain} -ip > subfinder.{domain}.csv"
    # Chạy lệnh nhưng không hiển thị kết quả trực tiếp trên terminal
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Running: {command}...")
    stdout, stderr = process.communicate()

    new_line = "subdomain,ip,source\n"
    with open(f"subfinder.{domain}.csv", 'r') as file:
        old_content = file.read()
    if not old_content.startswith("subdomain,ip,source"):   
        with open(f"subfinder.{domain}.csv", 'w') as file:
            file.write(new_line + old_content)

    filter(f"{domain}.csv",f"subfinder.{domain}.csv")

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

def alertNew(message,chat_id='-4069733583'):
    echo_bot.bot.send_message(chat_id=chat_id, text=message)

def alertSub():
    pass

def checkStatus():
    # update cả status của những cái cũ (trước mắt là update những cái die, lập lịch để check)
    pass

def main():
    domain = 'bizflycloud.vn'
    # filter(f"{domain}.csv",f"subfinder.{domain}.csv")
    tool(domain)

main()
