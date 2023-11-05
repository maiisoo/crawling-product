import csv

import requests as requests
from bs4 import BeautifulSoup
from utils import get_random_agent, no_accent_vietnamese

headers = {
            "User-Agent": get_random_agent()
        }

#Cho url vào đây
#   VD url = "https://tiki.vn/xit-duong-toc/c11825"
# list sản phẩm nào mà có >=2 trang thì viết thêm param vào
#   VD: url = "https://tiki.vn/xit-duong-toc/c11825?page=2"

url = "https://tiki.vn/xit-duong-toc/c11825"
#nếu có <số trang> thì viết vào biến pageNum này
pageNumber = ""

html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, features="html.parser")

try:
    category = soup.find('div', class_='title').text
    print(category)
except:
    category = "" #Lỗi thì tự điền tên danh mục

#Bỏ cách đầu cuối
category = category.strip()

print(category+"1")

product_names = [element.h3.text for element in soup.find_all('div', class_='name')]

product_data = []

for product_name in product_names:
    print(product_name) #In ra xem đúng chưa
    product_data.append((category, product_name))

#Đặt tên file csv
noAccentCategory = no_accent_vietnamese(category).replace(' ', '_')
if pageNumber != "":
    filename = noAccentCategory + "_" + pageNumber + ".csv"
else:
    filename = noAccentCategory + ".csv"
print(filename)

# Viết ra csv, mỗi category 1 file riêng
with open(f'data/{filename}', 'w', newline='', encoding='utf-8') as filepath:
    csv_writer = csv.writer(filepath)
    csv_writer.writerows(product_data)
