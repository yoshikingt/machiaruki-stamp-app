from route import app
import os

if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_RUN_HOST'), port=os.getenv('FLASK_RUN_PORT'))
