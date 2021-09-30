from db import db
import users


def show_all():
    sql = "SELECT id, header FROM listings ORDER BY id DESC"
    result = db.session.execute(sql)
    headers =  result.fetchall()
    return headers

def post_object(header, location, content, user_id):
    #user_id = users.user_id
    #if user_id == 0:
    #    return False
    sql = "INSERT INTO listings (header, location, content, user_id) VALUES (:header, :location, :content, :user_id)"
    db.session.execute(sql, {"header":header, "location":location, "content":content, "user_id":user_id})
    db.session.commit()
    return True

def show_object(id):
    sql = "SELECT header, location, content, user_id FROM listings WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    object = result.fetchall()
    return object

def my_items(user_id):
    sql = "SELECT * FROM listings WHERE user_id=:user_id" 
    result = db.session.execute(sql, {"user_id":user_id})
    myitems = result.fetchall()
    return myitems