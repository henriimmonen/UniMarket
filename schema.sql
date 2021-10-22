CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
CREATE TABLE listings (id SERIAL PRIMARY KEY , header TEXT, location TEXT, content TEXT, user_id INTEGER REFERENCES users(id), price INTEGER, visible BOOLEAN);
CREATE TABLE photos (id SERIAL PRIMARY KEY, name TEXT, data BYTEA, item_id INTEGER REFERENCES listings(id));
CREATE TABLE comments (id SERIAL PRIMARY KEY, content TEXT, poster_id INTEGER REFERENCES users(id), item_id INTEGER REFERENCES listings(id), sent_at TIMESTAMP);
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, sent_at TIMESTAMP, sent_by INTEGER REFERENCES users(id), sent_to INTEGER REFERENCES users(id));