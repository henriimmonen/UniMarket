from db import db


def show_all():
    sql = "SELECT id, header FROM listings ORDER BY id DESC"
    result = db.session.execute(sql)
    headers =  result.fetchall()
    return headers

def post_object(header, location, content):
    sql = "INSERT INTO listings (header, location, content) VALUES (:header, :location, :content)"
    db.session.execute(sql, {"header":header, "location":location, "content":content})
    db.session.commit()

def show_object(id):
    sql = "SELECT header, location, content FROM listings WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    object = result.fetchall()
    return object