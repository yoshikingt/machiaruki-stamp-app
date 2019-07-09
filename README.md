# 沼津まちあるきスタンプ一覧出力アプリ machiaruki-stamp

沼津まちあるきスタンプの設置箇所と店舗詳細を csv ファイルに出力します。

Google Spread Sheet を指定することで、そちらに出力することもできます。

The installation location and store details of Numazu machiuki stamp are output to a csv file.

You can also output to Google Spread Sheet by specifying it.

## Google Sheet API credentials が必要です Requires Google Sheet API credentials

これは現時点ではアプリの動作に必須ですが、将来的にオプションにする予定です。

1. ご自身の Google アカウントで Google Sheet API を有効にします。
2. JSON 形式の credentials を作成します。
3. 作成した credentials ファイルを `runserver.py` と同一のディレクトリに配置してください。
4. 配置した credentials ファイルを `credentials.json` にリネームしてください。

This is essential to the operation of the app at this time, but it will be an option in the future.

1. Enable Google Sheet API on your Google Account.
2. Create API credentials. (json)
3. Put credentials json on same directory as `runserver.py`.
4. Rename credentials json to `credentials.json`.

## アプリの動作に必要ないくつかの設定です Requires some settings

1. `config.ini` の内容を、以下のように変更します。
  - sheet_id : ここに出力先の Google Spreadsheet id を入力してください。

1. Editing `config.ini`.
  - sheet_id : Your Google Spreadsheet id

## Docker コンテナでの動かし方 How to Running on Docker container

1. docker image をビルド
`docker-compose build`
2. docker container を起動
`docker-compose up`

1. Build to image
`docker-compose build`
2. Run the Container
`docker-compose up`
