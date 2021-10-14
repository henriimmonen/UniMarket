from app import app
from flask import render_template, request, redirect
import users, items


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/sell")
def formToPost():
	return render_template("selling_form.html")

@app.route("/send", methods=["POST"])
def postObject():
	users.check_csrf()
	header = request.form["header"]
	location = request.form["location"]
	content = request.form["content"]
	user_id = users.user_id()
	if items.post_object(header, location, content, user_id):
		return redirect("/showAll")
	else:
		return redirect("/showAll")

@app.route("/showAll")
def showAll():
	headers = items.show_all()
	return render_template("showAll.html", headers=headers)

@app.route("/object/<int:id>")
def showObject(id):
	if items.show_object(id):
		object = items.show_object(id)
		comments = items.show_comments(id)
		return render_template("object.html",id=id, object=object, comments=comments)
	else: 
		return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")

	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if not users.login(username, password):
			return render_template("index.html")

		return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")

	if request.method == "POST":
		username = request.form["username"]
		if len(username) < 1 or len(username) > 20:
			error = "Something is wrong with the username"
			return render_template("error.html", error=error)

		password1 = request.form["password1"]
		password2 = request.form["password2"]

		if password1 != password2:
			error = "Passwords differ"
			return render_template("error.html", error=error)
		if password1 == "" or password2 == "":
			error = "Password empty"
			return render_template("error.html", error=error)
		if not users.register(username, password1):
			error = "Something went wrong!"
			return render_template("error.html", error=error)
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

@app.route("/postphoto", methods=["POST"])
def photo():
	users.check_csrf()
	file = request.files["file"]
	name = file.filename
	item_id = request.form["id"]
	items.post_photo(file, name, item_id)
	return redirect("/object/" + str(item_id))

@app.route("/object/<int:id>/photo")
def postPhoto(id):
	return render_template("photo.html", id=id)

@app.route("/showphoto/<int:id>")
def showPhoto(id):
	object = items.show_photo(id)
	return object

@app.route("/query")
def query():
	query = request.args["query"]
	query_result = items.make_query(query)
	return render_template("result.html", query_result = query_result)
	
@app.route("/sendComment", methods=["POST"])
def comment():
	item_id = request.form["id"]
	user_id = users.user_id()
	comment = request.form["comment"]
	items.comment(item_id, user_id, comment)
	return redirect("/object/" + str(item_id))
