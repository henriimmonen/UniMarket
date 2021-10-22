from app import app
from flask import render_template, request, redirect
import users, items

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")

	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if not users.login(username, password):
			error = "Login failed"
			return render_template("error.html", error=error)
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
		users.login(username, password1)
		return redirect("/")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")

@app.route("/sell")
def form_to_post():
	return render_template("selling_form.html")

@app.route("/send", methods=["POST"])
def post_object():
	users.check_csrf()
	header = request.form["header"]
	if len(header) < 1:
		error = "Please enter a title for the item"
		return render_template("error.html", error=error)
	location = request.form["location"]
	if len(location) < 1:
		error = "Please enter a location for the item"
		return render_template("error.html", error=error)
	price = int(request.form["price"])
	if price < 0 or not isinstance(price, int):
		error = "Please enter a valid price"
		return render_template("error.html", error=error)
	content = request.form["content"]
	if len(content) < 1:
		error = "Please enter description of the item"
		return render_template("error.html", error=error)
	user_id = users.user_id()
	if items.post_object(header, location, content, user_id, price):
		return redirect("/showall")
	else:
		error = "Object not posted"
		return render_template("error.html",error=error)

@app.route("/showall")
def show_all():
	all_items = items.show_all()
	return render_template("show_all.html", all_items=all_items)

@app.route("/object/<int:id>")
def show_object(id):
	if items.show_object(id):
		object = items.show_object(id)
		comments = items.show_comments(id)
		return render_template("object.html",id=id, object=object, comments=comments)
	else: 
		return redirect("/")

@app.route("/object/<int:id>/delete", methods=["GET"])
def delete_item(id):
	if items.check_id(users.user_id()):
		items.delete_item(id)
		return redirect("/myitems")
	else:
		error = "Not able to delete item"
		return render_template("error.html", error=error)

@app.route("/myitems")
def my_items():
	user_id = users.user_id()
	myitems = items.my_items(user_id)
	return render_template("myitems.html", myitems=myitems)

@app.route("/postphoto", methods=["POST"])
def photo():
	users.check_csrf()
	file = request.files["file"]
	name = file.filename
	item_id = request.form["id"]
	if items.post_photo(file, name, item_id):
		return redirect("/object/" + str(item_id))
	else:
		error = "Failed to post a photo"
		return render_template("error.html", error=error)

@app.route("/object/<int:id>/postphoto", methods=["GET"])
def post_photo_form(id):
	if not items.check_id(users.user_id()):
		error = "This isn't your object"
		return render_template("error.html", error=error)
	return render_template("photo.html", id=id)

@app.route("/object/<int:id>/showphoto")
def show_photo(id):
	if items.show_photo(id):
		object = items.show_photo(id)
		return object
	else:
		error = "No photo yet"
		return render_template("error.html", error=error)

@app.route("/query")
def query():
	query = request.args["query"]
	query_result = items.make_query(query)
	return render_template("result.html", query_result = query_result)

@app.route("/sendcomment", methods=["POST"])
def comment():
	item_id = request.form["id"]
	user_id = users.user_id()
	comment = request.form["comment"]
	items.comment(item_id, user_id, comment)
	return redirect("/object/" + str(item_id))

@app.route("/userinfo", methods=["GET"])
def user_information():
	user_id = users.user_id()
	username = users.user_name(user_id)
	messages_to_user = users.get_messages(user_id)
	messages_sent_by_user = users.get_sent_messages(user_id)
	return render_template("userinformation.html", username=username, 
		messages=messages_to_user, sent_messages=messages_sent_by_user)

@app.route("/sendmessage", methods=["GET"])
def private_message():
	return render_template("private_message.html")

@app.route("/postmessage", methods=["GET","POST"])
def post_message():
	if request.method == "GET":
		return redirect("/")
	else:
		sent_to_username = request.form["username"]
		sent_to = users.other_user_id(sent_to_username)
		content = request.form["content"]
		sent_by = users.user_id()
		users.check_csrf()
		if users.send_private_message(content, sent_by, sent_to):
			return redirect("/userinfo")
		else:
			error = "Message not sent"
			return render_template("error.html", error=error)
