from flask import Flask, jsonify
from flask_cors import CORS
import main

app = Flask(__name__)
CORS(app)

@app.route('/api/stamps', methods=['PUT'])
def index():
    main.main()
    return jsonify({"message": "done"})

@app.route('/api', methods=['GET'])
def test():
    return jsonify({"message": "reached"})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
