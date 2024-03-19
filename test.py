import os
import csv

# Đường dẫn tới thư mục chứa các file domain.csv
folder_path = "data"

# Lặp qua các file trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        # Trích xuất tên miền từ tên file
        domain_name = filename.replace(".csv", "")
        
        file_path = os.path.join(folder_path, filename)
        
        # Mở file CSV và thêm dòng mới
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([domain_name, "1.1.1.1", "kk"])
