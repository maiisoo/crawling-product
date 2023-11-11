import csv
import re
import requests as requests
from bs4 import BeautifulSoup
from utils import get_random_agent, no_accent_vietnamese
import json

headers = {
            "User-Agent": get_random_agent()
        }

#Cho url vào đây
#   VD url = "https://tiki.vn/xit-duong-toc/c11825"
# list sản phẩm nào mà có >=2 trang thì viết thêm param vào
#   VD: url = "https://tiki.vn/xit-duong-toc/c11825?page=2"

def getDataByCategory(category, pageNum):
    product_data = []
    label = category.replace(" ", "_")
    label = "__label__" + label
    for pageNumber in range(1, pageNum+1):
        url = "https://tiki.vn/search?q=" + category + "&page=" + str(pageNumber)
        print(url)

        html = requests.get(url, headers=headers)
        # check request valid
        if html.status_code != 200:
            print("Error: " + str(html.status_code))
            exit(1)
        soup = BeautifulSoup(html.text, features="html.parser")
        
        # data = json.loads(soup.find('script', type='application/ld+json').text)

        #list of script objects
        scriptList = soup.find_all('script', type='application/ld+json')

        scriptDictList = []
        for i in scriptList:
            scriptDictList.append(json.loads(i.text))
            # dict dont have key "name":
            # if "name" not in i.text:
            #     scriptDictList.remove(i)

        #filter items that dont have key "name"
        filtered_list = [d for d in scriptDictList if "name" in d]

        product_names=[]
        for i in filtered_list:
            product_names.append(i["name"])
        
        for product_name in product_names:
            product_data.append((label, product_name))
            print(product_data[-1])

    #Đặt tên file csv
    filename = ""
    noAccentCategory = no_accent_vietnamese(category).replace(' ', '_').replace('/', '_')
    filename = noAccentCategory + ".csv"
    print(filename)

    with open(f'data_tiki/{filename}', 'w', newline='', encoding='utf-8') as filepath:
        csv_writer = csv.writer(filepath)
        csv_writer.writerows(product_data)


categories = []

f = open("categories.txt", "r", encoding="utf8")
while True:
    line = f.readline()
    if not line:
        break
    line = line.strip().replace("\n", "")
    categories.append(line)

# Sửa index tại đây: 1000, 1971
for i in range(992, 1000):
    getDataByCategory(categories[i], 5)