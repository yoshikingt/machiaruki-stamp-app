import re
import csv
import requests
from bs4 import BeautifulSoup

# ソース取得
r = requests.get('https://www.llsunshine-numazu.jp/')
html = r.content
soup = BeautifulSoup(html, 'html.parser')
shopList = soup.find_all('dl', class_=re.compile('^shop_st'))

outputList = []
outputList.append(['Name', 'Info', 'Link']) # ヘッダ

# スタンプ設置箇所ごとに処理
for shop in shopList:
    name = shop.dt.text
    info = shop.dd.text.replace('\n', ' ').replace('\r', ' ')
    link = ''
    if shop.find('a') is not None: # リンクがない場合の対策
        link = shop.find('a').get('href')
    outputList.append([name, info, link])

# CSV として書き出し
with open('shop_list.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(outputList)
