import os
import flask
from flask import g, make_response,render_template,request,redirect
import sqlite3
import requests

DATABASE = 'database.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = flask.Flask(__name__)
from flask_cors import CORS
CORS(app)
app.config.update(
    SECRET_KEY="Harsh-Secet!",
    SESSION_COOKIE_SAMESITE='Strict',
    UPLOAD_FOLDER=UPLOAD_FOLDER
)


requests.default_timeout = 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def write_db(query, args=()):
    """
    Helper Method for Write
    """
    db = get_db()
    db.execute(query, args)
    db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('../schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
def shemainsert():
    with app.app_context():
        db = get_db()
        with app.open_resource('../schema2.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()