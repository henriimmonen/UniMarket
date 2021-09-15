from flask import Flask
from flask import render_template
app = Flask(__name__)

# First page for 'UniMarket' - Still in Development!

@app.route("/")
def index():
    return render_template("index.html")
