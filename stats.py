from db import db

def amount_of_items():
    sql = "SELECT COUNT(id) FROM listings WHERE visible='TRUE'"
    result = db.session.execute(sql)
    amount = result.fetchone()[0]
    return amount

def avg_price_hki():
    sql = "SELECT AVG(price) FROM listings WHERE UPPER(location) LIKE UPPER('%Helsinki%')"
    result = db.session.execute(sql)
    average = result.fetchone()[0]
    return average

def total_users():
    sql = "SELECT COUNT(id) FROM users"
    result = db.session.execute(sql)
    amount = result.fetchone()[0]
    return amount

def total_sum():
    sql = "SELECT SUM(price) FROM listings WHERE visible='TRUE'"
    result = db.session.execute(sql)
    total_sum = result.fetchone()[0]
    return total_sum

def min_price():
    sql = "SELECT MIN(price) FROM listings WHERE visible='TRUE'"
    result = db.session.execute(sql)
    min_price = result.fetchone()[0]
    return min_price

def max_price():
    sql = "SELECT MAX(price) FROM listings WHERE visible='TRUE'"
    result = db.session.execute(sql)
    max_price = result.fetchone()[0]
    return max_price

def sold_items_per_user():
    sql = "SELECT u.username, COUNT(l.id) AS item_count FROM listings l, users u WHERE l.visible='FALSE' AND u.id = l.user_id GROUP BY u.username"
    result = db.session.execute(sql)
    sold_items = result.fetchall()
    return sold_items