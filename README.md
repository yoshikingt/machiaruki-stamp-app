# machiaruki-stamp

## Requires Google Sheet API credentials

1. Enable Google Sheet API on your Google Account.
2. Create API credenatials. (json)
3. Put credenatials json on same directory as `main.py`.
4. Rename credentials json to `credentials.json`.

## Requires some settings

1. Editing `config.ini`.
  - sheet_id : Your Google Spreadsheet id

## How to Running on Docker container (optional)

1. Build to image
`docker image build -t sample:latest .`
2. Run the Container
`docker container run -it --rm -p 5000:5000 --name run-sample sample`
