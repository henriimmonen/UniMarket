from db import db
import users
from flask import make_response, render_template

def show_all():
    sql = "SELECT id, header, location FROM listings ORDER BY id DESC"
    result = db.session.execute(sql)
    all_items =  result.fetchall()
    return all_items

def post_object(header, location, content, user_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO listings (header, location, content, user_id) VALUES (:header, :location, :content, :user_id)"
    db.session.execute(sql, {"header":header, "location":location, "content":content, "user_id":user_id})
    db.session.commit()
    return True

def post_photo(file, name, item_id):
    if not name.endswith(".jpg"):
        return False
    data = file.read()
    if len(data) > 5000*5000:
        return False
    sql = "INSERT INTO photos (name,data, item_id) VALUES (:name,:data, :item_id)"
    db.session.execute(sql, {"name":name, "data":data, "item_id":item_id})
    db.session.commit()
    return True

def show_object(id):
    sql = "SELECT header, location, content, user_id, id FROM listings WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    object = result.fetchall()
    return object

def show_comments(id):
    sql1 = "SELECT c.content, c.sent_at, u.username FROM comments c, users u WHERE item_id=:id AND u.id=c.poster_id "
    result1 = db.session.execute(sql1, {"id":id})
    comments = result1.fetchall()
    return comments

def my_items(user_id):
    sql = "SELECT * FROM listings WHERE user_id=:user_id" 
    result = db.session.execute(sql, {"user_id":user_id})
    myitems = result.fetchall()
    return myitems

def show_photo(id):
    try:
        sql = "SELECT data FROM photos WHERE item_id=:id"
        result = db.session.execute(sql, {"id":id})
        data = result.fetchone()[0]
        response = make_response(bytes(data))
        response.headers.set("Content-Type","image/jpeg")
        return response
    except:
        error = "Photo download unsuccessful"
        return render_template("error.html", error=error)

def make_query(query):
    sql = "SELECT id, header FROM listings WHERE header LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    items = result.fetchall()
    return items

def comment(item_id, user_id, comment):
    try:
        sql = "INSERT INTO comments (content, poster_id, item_id, sent_at) VALUES (:content, :user_id, :item_id, NOW())"
        db.session.execute(sql, {"content":comment, "user_id":user_id, "item_id":item_id})
        db.session.commit()
    except:
        error = "Something went wrong"
        return render_template("error.html", error=error)

