import re
import csv
import requests
import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials


def scraping(url):
    r = requests.get(url)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('dl', class_=re.compile('^shop_st'))


def create_data(shop_list):
    output_list = []
    output_list.append(['押印', '店名', 'メンバー', '住所', '営業時間', '定休日', '備考', 'リンク']) # ヘッダ
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
        output_list.append(['', name, member, address, opening, closed, note, link])
    return output_list


def output_csv(filepath, output_list):
    with open(filepath, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(output_list)


def connect_spreadsheet(filepath):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(filepath, scope)
    return gspread.authorize(credentials)


def update_spreadsheet(worksheet, output_list):
    cell_list = worksheet.range(1, 1, len(output_list), len(output_list[0]))
    tmp_list = [value for row in output_list for value in row] # 2次元配列を1次元配列に詰め替え
    for cell, value in zip(cell_list, tmp_list):
        cell.value = value
    worksheet.update_cells(cell_list)
