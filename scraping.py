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
outputList.append(['Name', 'Member', 'Address', 'Opening', 'Closed', 'Note', 'Link']) # ヘッダ

# スタンプ設置箇所ごとに処理
for shop in shopList:
    name = shop.dt.text
    info = shop.dd.text.replace('\n', ' ').replace('\r', ' ')
    member = re.compile('メンバー／.*?住所').search(info).group(0).replace('メンバー／', '').replace('住所', '')
    address = re.compile('住所／.*?営業時間').search(info).group(0).replace('住所／', '').replace('営業時間', '')
    opening = re.compile('営業時間／.*?定休日').search(info).group(0).replace('営業時間／', '').replace('定休日', '')
    closed = re.sub('※.*', '', re.compile('定休日／.*').search(info).group(0).replace('定休日／', '').replace('店舗のホームページを見る', ''))
    note = ''
    if re.compile('※.*').search(info) is not None: # 注記がない場合の対策
        note = re.compile('※.*').search(info).group(0).replace('店舗のホームページを見る', '')
    link = ''
    if shop.find('a') is not None: # リンクがない場合の対策
        link = shop.find('a').get('href')
    outputList.append([name, member, address, opening, closed, note, link])

# CSV として書き出し
with open('shop_list.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(outputList)
