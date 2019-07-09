from flask import Flask
from flask import jsonify
from flask_cors import CORS
import configparser
import function

app = Flask(__name__)
CORS(app)


@app.route('/api/stamps', methods=['POST'])
def post_stamps():
    SCRAPING_TARGET = 'https://www.llsunshine-numazu.jp/'
    CSV_FILE_PATH = 'shop_list.csv'
    config = configparser.ConfigParser()
    config.read('config.ini')
    SHEET_ID = config.get('DEFAULT', 'sheet_id')
    CREDENTIAL_FILE_PATH = 'credentials.json'

    # ソース取得
    shop_list = function.scraping(SCRAPING_TARGET)
    # データ作成
    output_list = function.create_data(shop_list)
    # CSV として書き出し
    function.output_csv(CSV_FILE_PATH, output_list)
    # Google Spreadsheet に接続
    gc = function.connect_spreadsheet(CREDENTIAL_FILE_PATH)
    worksheet = gc.open_by_key(SHEET_ID).sheet1
    # Google Spreadsheet 更新
    function.update_spreadsheet(worksheet, output_list)

    return jsonify({"message": "done"})


@app.route('/api', methods=['GET'])
def check_reached():
    return jsonify({"message": "reached"})


if __name__ == '__main__':
    # 開発作業中以外はコメントアウト
    # app.run(debug=True)
    # 開発作業中のみコメントアウト
    app.run(host='0.0.0.0', port=5000)
