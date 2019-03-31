import flask
import main

app = flask.Flask(__name__)

@app.route('/api/stamps', methods=['PUT'])
def index():
    main.main()
    return 'done'

if __name__ == '__main__':
    app.run(debug=True)
