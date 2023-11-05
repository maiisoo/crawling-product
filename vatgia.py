import csv
import re

import requests as requests
from bs4 import BeautifulSoup
from utils import get_random_agent, no_accent_vietnamese

headers = {
            "User-Agent": get_random_agent()
        }

#Cho url vào đây
#   VD url = "https://vatgia.com/10757/dong-ho-thong-minh-smartwatch.html"
# list sản phẩm nào mà có >=2 trang thì viết url+,<số trang>
#   VD: url = https://vatgia.com/10757/dong-ho-thong-minh-smartwatch.html,2

url = "https://vatgia.com/10757/dong-ho-thong-minh-smartwatch.html"
#nếu có <số trang> thì viết vào biến pageNum này
pageNumber = ""
html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, features="html.parser")

pattern_matching = re.search(r'/(\d+)/', url)
try:
    index = pattern_matching.group(1)
    print(index)
    category = soup.find('a', idata=index).text
    print(category)
except:
    category = "" #Lỗi index trên thì tự điền tên danh mục

# Bỏ cách đầu cuối
category = category.strip()

product_names = [element.a.text for element in soup.find_all('div', class_='name')]

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
