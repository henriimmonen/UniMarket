CREATE TABLE listings (id SERIAL PRIMARY KEY , header TEXT, location TEXT, content TEXT, user_id INTEGER REFERENCES users(id));
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, admin BOOLEAN);
