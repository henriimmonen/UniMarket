CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
CREATE TABLE listings (id SERIAL PRIMARY KEY , header TEXT, location TEXT, content TEXT, user_id INTEGER REFERENCES users(id));
CREATE TABLE photos (id SERIAL PRIMARY KEY, name TEXT, data BYTEA, item_id INTEGER REFERENCES listings(id));
