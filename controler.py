
import subprocess
import config as cf
import pandas as pd

def extract_first_column_to_txt(dataframe, output_file):
    first_column_values = dataframe.iloc[1:, 0]  # Lấy giá trị cột đầu tiên từ dòng thứ hai trở đi
    first_column_values.to_csv(output_file, index=False, header=False)

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
    extract_first_column_to_txt(merged_df,oldFile.replace("data/", "data_txt/").replace(".csv", ".txt"))
    return new_subdomain
    # if new_subdomain != '':
    #     alertNew(new_subdomain)
    
    # print(new_subdomain)


def subfinder(domain):
    command = f"{cf.SUBFINDER} -active -all -d {domain} -ip > tmp_data/subfinder.{domain}.csv" # chạy service thì cần đường dẫn tuyệt đối của tool
    # Chạy lệnh nhưng không hiển thị kết quả trực tiếp trên terminal
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Running: {command}...")
    process.wait()
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

def tool(domain='bizflycloud.vn',type=1): # tổng hợp từ một số tool -> chạy đa luồng, mỗi luồng một tool
    # chạy tools
    subfinder(domain)

    if type == 0:
        return ''
    # filter kết quả
    new_subdomain = filter(f"data/{domain}.csv",f"tmp_data/subfinder.{domain}.csv")
    return new_subdomain