import re
import csv
import requests
import gspread
import configparser
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

config = configparser.ConfigParser()
config.read('config.ini')
SHEET_ID = config.get('DEFAULT' ,'sheet_id')
CREDENTIAL_FILE_PATH = 'credentials.json'

# ソース取得
r = requests.get('https://www.llsunshine-numazu.jp/')
html = r.content
soup = BeautifulSoup(html, 'html.parser')
shop_list = soup.find_all('dl', class_=re.compile('^shop_st'))

output_list = []
output_list.append(['Name', 'Member', 'Address', 'Opening', 'Closed', 'Note', 'Link']) # ヘッダ

# スタンプ設置箇所ごとに処理
for shop in shop_list:
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
    output_list.append([name, member, address, opening, closed, note, link])

# CSV として書き出し
with open('shop_list.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(output_list)

# Google Spreadsheet に接続
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIAL_FILE_PATH, scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_key(SHEET_ID).sheet1

# セルを範囲指定して一括更新
cell_list = wks.range(1, 1, len(output_list), 7)
tmp_list = [value for row in output_list for value in row] # 2次元配列を1次元配列に詰め替え
for cell, value in zip(cell_list, tmp_list):
    cell.value = value
wks.update_cells(cell_list)
