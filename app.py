from flask import Flask

app = Flask(__name__)

# First page for 'UniMarket' - Still in Development!

@app.route("/")
def index():
    return "Work in progress"
