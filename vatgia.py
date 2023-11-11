import csv
import re

import requests as requests
from bs4 import BeautifulSoup
from utils import get_random_agent, no_accent_vietnamese

headers = {
            "User-Agent": get_random_agent()
        }

def getDataByCategory(category, pageNumber):
    product_data = []
    label = category.replace(" ", "_")
    label = "__label__" + label
    for num in range(1, pageNumber+1):
        url = "https://vatgia.com/home/" + category.replace(" ", "+") + ".spvg?page=" + str(num)
        print(url)
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, features="html.parser")

        pattern_matching = re.search(r'/(\d+)/', url)

        product_names = [element.a.text for element in soup.find_all('div', class_='name')]


        for product_name in product_names:
            # print(product_name) #In ra xem đúng chưa
            product_data.append((label, product_name))
            # print product_name
            print(product_name);


    #Đặt tên file csv
    noAccentCategory = no_accent_vietnamese(category).replace(' ', '_').replace('/', '_')
    filename = noAccentCategory + ".csv"
    print(filename)
    # f = open(f'data/{filename}', 'w', newline='', encoding='utf-8')
    #f.writelines(f'{product_data}\n')
    # Viết ra csv, mỗi category 1 file riêng
    # product_data["category"] = ("__label__" + product_data["category"]).replace(" ", "_")


    with open(f'data_vatgia/{filename}', 'w', newline='', encoding='utf-8') as filepath:
        csv_writer = csv.writer(filepath)
        csv_writer.writerows(product_data)

# getDataByCategory("Điện thoại", 5)

categories = []

f = open("categories.txt", "r", encoding="utf8")
while True:
    line = f.readline()
    if not line:
        break
    line = line.strip().replace("\n", "")
    categories.append(line)

# Sửa index tại đây: 1000, 1971
for i in range(347, 348):
    getDataByCategory(categories[i], 5)