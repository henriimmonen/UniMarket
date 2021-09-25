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
	header = request.form["header"]
	location = request.form["location"]
	content = request.form["content"]
	sql = "INSERT INTO listings (header, location, content) VALUES (:header, :location, :content)"
	db.session.execute(sql, {"header":header, "location":location, "content":content})
	db.session.commit()
	return redirect("/showAll")

@app.route("/showAll")
def showAll():
	sql = "SELECT id, header FROM listings ORDER BY id DESC"
	result = db.session.execute(sql)
	headers =  result.fetchall()
	return render_template("showAll.html", count=len(headers), headers=headers)

@app.route("/object/<int:id>")
def showObject(id):
	sql = "SELECT header, location, content FROM listings WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	object = result.fetchall()
	return render_template("object.html", object=object)
