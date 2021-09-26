from app import app
from flask import render_template, request, redirect, session
import users, items


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
	user_id = users.user_id()
	if items.post_object(header, location, content, user_id):
		return redirect("/showAll")
	else:
		error = "Post object failed"
		return redirect("/showAll")

@app.route("/showAll")
def showAll():
	headers = items.show_all()
	return render_template("showAll.html", count=len(headers), headers=headers)

@app.route("/object/<int:id>")
def showObject(id):
	if items.show_object(id):
		object = items.show_object(id)
	else:
		error = "Something went wrong"
	return render_template("object.html", object=object)

@app.route("/login", methods=["GET", "POST"])
def login():
	error = None
	if request.method == "GET":
		return render_template("login.html")

	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if not users.login(username, password):
			error = "Not able to log in"
			return render_template("index.html")

		return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
	error = None
	if request.method == "GET":
		return render_template("register.html")

	if request.method == "POST":
		username = request.form["username"]
		if len(username) < 1 or len(username) > 20:
			error = "Username not applicable"
		password1 = request.form["password1"]
		password2 = request.form["password2"]

		if password1 != password2:
			error = "Passwords differ"
		if password1 == "":
			error = "Password empty"
		if not users.register(username, password1):
			error = "Was not able to register"
		return redirect("/")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")

@app.route("/myitems")
def myitems():
	user_id = users.user_id()
	myitems = items.my_items(user_id)
	return render_template("myitems.html", myitems=myitems)