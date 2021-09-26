from db import db
from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    error = None
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    hash_value = user.password  
    if not user:
        flash("Invalid username!")
        return False

    if not check_password_hash(hash_value, password):
        flash("Invalid password!")
        return False
    
    flash("You were successfully logged in!")
    session["user_id"] = user[1]
    session["user_name"] = username
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False

    return login(username, password)
	


