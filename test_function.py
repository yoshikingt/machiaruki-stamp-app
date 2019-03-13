import unittest
import re
from bs4 import BeautifulSoup
import function

class TestFunction(unittest.TestCase):

    # 全ての項目がある場合、期待通り出力されること
    def test_create_data_01(self):
        shop_list = create_source(
            '<dl class="shop_st14">'\
                '<dt class="shop14">浜忠</dt>'\
                '<dd>'\
                    '<strong>メンバー／黒澤ルビィ</strong>'\
                    '住所／沼津市上土町80<br>'\
                    '営業時間／昼　11:30～15:00<br>'\
                    '夜　17:00～22:00<br>'\
                    '定休日／月曜日<br>'\
                    '※スタンプ店内設置の為、営業時間内にお越しください'\
                    '<a href="http://www4.tokai.or.jp/hamatyuu/" target="_blank" class="link_shop">店舗のホームページを見る</a>'\
                '</dd>'\
            '</dl>'
        )
        actual_list = function.create_data(shop_list)
        expected_list = create_expected(
            [''
            , '浜忠'
            , '黒澤ルビィ'
            , '沼津市上土町80'
            , '昼　11:30～15:00夜　17:00～22:00'
            , '月曜日'
            , '※スタンプ店内設置の為、営業時間内にお越しください'
            , 'http://www4.tokai.or.jp/hamatyuu/']
        )
        self.assertEqual(actual_list, expected_list)

    # 備考がない場合、失敗せずに期待通り出力されること
    def test_create_data_02(self):
        shop_list = create_source(
            '<dl class="shop_st10">'\
                '<dt class="shop10">JAなんすん（沼津みなと新鮮館内）</dt>'\
                '<dd>'\
                    '<strong>メンバー／高海千歌</strong>'\
                    '住所／沼津市千本港町128-1　沼津みなと新鮮館内<br/>'\
                    '営業時間／9:30～16:30<br/>'\
                    '定休日／第2第4火曜日'\
                    '<a class="link_shop" href="http://www.ja-nansun.or.jp/" target="_blank">店舗のホームページを見る</a>'\
                '</dd>'\
            '</dl>'\
        )
        actual_list = function.create_data(shop_list)
        expected_list = create_expected(
            [''
            , 'JAなんすん（沼津みなと新鮮館内）'
            , '高海千歌'
            , '沼津市千本港町128-1　沼津みなと新鮮館内'
            , '9:30～16:30'
            , '第2第4火曜日'
            , ''
            , 'http://www.ja-nansun.or.jp/']
        )
        self.assertEqual(actual_list, expected_list)

    # リンクがない場合、失敗せずに期待通り出力されること
    def test_create_data_03(self):
        shop_list = create_source(
            '<dl class="shop_st13">'\
              '<dt class="shop13">JEWELRY＆WATCH 市川</dt>'\
                '<dd>'\
                    '<strong>メンバー／黒澤ダイヤ</strong>'\
                    '住所／沼津市上土町100-1<br>'\
                    '営業時間／10:00～19:00<br>'\
                    '定休日／水曜日'\
                '</dd>'\
            '</dl>'
        )
        actual_list = function.create_data(shop_list)
        expected_list = create_expected(
            [''
            , 'JEWELRY＆WATCH 市川'
            , '黒澤ダイヤ'
            , '沼津市上土町100-1'
            , '10:00～19:00'
            , '水曜日'
            , ''
            , '']
        )
        self.assertEqual(actual_list, expected_list)


def create_source(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('dl', class_=re.compile('^shop_st'))

def create_expected(expected):
    expected_list = []
    expected_list.append(['押印', '店名', 'メンバー', '住所', '営業時間', '定休日', '備考', 'リンク'])
    expected_list.append(expected)
    return expected_list
