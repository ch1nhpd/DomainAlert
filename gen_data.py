
# khởi tạo dữ liệu gốc
import os

# Đường dẫn tới thư mục data
folder_path = os.getcwd() + "/data"

# Đọc danh sách tên domain từ file listdomain.txt
with open("listdomain.txt", "r") as file:
    domain_names = file.readlines()

# Lặp qua từng tên domain và tạo file CSV tương ứng
for domain_name in domain_names:
    domain_name = domain_name.strip()  # Loại bỏ dấu xuống dòng từ danh sách
    file_name = f"{domain_name}.csv"
    file_path = os.path.join(folder_path, file_name)
    
    # Tạo file CSV mới và khởi tạo dữ liệu
    if not os.path.isfile(file_path):
        with open(file_path, "w") as csv_file:
            csv_file.write("Domain,IP,Status\n")
            csv_file.write(domain_name+",1.1.1.1,origin\n")
        # tạo luôn file txt
        open(folder_path+"_txt/"+domain_name+".txt", 'w').close()

