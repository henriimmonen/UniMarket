from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# First page for 'UniMarket' - Still in Development!

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def formToPost():
	return render_template("/form")

@app.route("/list", methods=["POST"])
def list():
	content = request.form["message"]
	sql = "INSERT INTO listings (content) VALUES (:content)"
	db.session.execute(sql, {"content":content})
	db.session.commit()
	return redirect("/")

@app.route("/show")
def showList():
	result = db.session.execute("SELECT content FROM listings")
	content = result.fetchall()
	return render_template("show.html", count=len(content), content=content)
