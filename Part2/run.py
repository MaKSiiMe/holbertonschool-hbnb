# filepath: /home/gioarias/holbertonschool-HBnB/Part2/run.py
from flask import Flask
from app.api.v1 import api
from app import create_app

app = create_app() # Create the Flask app
app = Flask(__name__)
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
