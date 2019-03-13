import re
import csv
import requests
import gspread
import configparser
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials


def func_scraping(url):
    r = requests.get(url)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('dl', class_=re.compile('^shop_st'))


def func_create_data(shop_list):
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
    return output_list


def func_output_csv(filepath):
    with open(filepath, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(output_list)


def func_connect_spreadsheet(filepath):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(filepath, scope)
    return gspread.authorize(credentials)


def func_update_spreadsheet(worksheet, output_list):
    cell_list = worksheet.range(1, 1, len(output_list), 7)
    tmp_list = [value for row in output_list for value in row] # 2次元配列を1次元配列に詰め替え
    for cell, value in zip(cell_list, tmp_list):
        cell.value = value
    worksheet.update_cells(cell_list)


SCRAPING_TARGET = 'https://www.llsunshine-numazu.jp/'
CSV_FILE_PATH = 'shop_list.csv'
config = configparser.ConfigParser()
config.read('config.ini')
SHEET_ID = config.get('DEFAULT' ,'sheet_id')
CREDENTIAL_FILE_PATH = 'credentials.json'

# ソース取得
shop_list = func_scraping(SCRAPING_TARGET)

# データ作成
output_list = func_create_data(shop_list)

# CSV として書き出し
func_output_csv(CSV_FILE_PATH)

# Google Spreadsheet に接続
gc = func_connect_spreadsheet(CREDENTIAL_FILE_PATH)
worksheet = gc.open_by_key(SHEET_ID).sheet1

# Google Spreadsheet 更新
func_update_spreadsheet(worksheet, output_list)
