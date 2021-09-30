from db import db
from flask import session, flash, secrets
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
    except:
        return False

    return login(username, password)

def user_id():
    return session.get("user_id",0)

def user_name(user_id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":user_id})
    name = result.fetchone()
    return name


