from flask import Flask, redirect
from flask import render_template, request
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
	return render_template("form.html")

@app.route("/send", methods=["POST"])
def postObject():
	title = request.form["header"]
	#location = request.form["location"]
	#content = request.form["content"]
	sql = "INSERT INTO listings (header) VALUES (:title)"
	db.session.execute(sql, {"title":title})
	db.session.commit()
	return redirect("/")

@app.route("/show")
def show():
	result = db.session.execute("SELECT header FROM listings")
	content = result.fetchall()
	return render_template("show.html", count=len(content), content=content)
