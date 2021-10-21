from db import db
from flask import session, flash, request, abort
import secrets
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        flash("Invalid username!")
        return False

    if not check_password_hash(user.password, password):
        flash("Invalid password!")
        return False
    
    flash("You were successfully logged in!")
    session["user_id"] = user[0]
    session["user_name"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["csrf_token"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False

def user_id():
    return session.get("user_id",0)

def user_name(user_id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":user_id})
    name = result.fetchone()[0]
    return name

def other_user_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    return user_id

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def get_messages(user_id):
    sql = "SELECT m.content, m.sent_at, u.username FROM messages m, users u WHERE sent_to=:id AND u.id=m.sent_by"
    result = db.session.execute(sql, {"id":user_id})
    messages = result.fetchall()
    return messages

def send_private_message(content, sent_by, sent_to):
    try:
        sql = "INSERT INTO messages (content, sent_at, sent_by, sent_to) VALUES (:content, NOW(), :sent_by, :sent_to)"
        db.session.execute(sql, {"content":content, "sent_by":sent_by, "sent_to":sent_to})
        db.session.commit()
        return True
    except:
        return False