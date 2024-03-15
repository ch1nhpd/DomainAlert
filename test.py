import subprocess
import config as cf
import pandas as pd

def extract_first_column_to_txt(dataframe, output_file):
    first_column_values = dataframe.iloc[:, 0]  # Lấy giá trị cột đầu tiên từ dòng thứ hai trở đi
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
domain = "bizflycloud.vn"
new_subdomain = filter(f"data/{domain}.csv",f"tmp_data/subfinder.{domain}.csv")