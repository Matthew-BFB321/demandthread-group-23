"""Connection to MySQL. Every other file reaches the database through the
helpers in this file."""
import os

import pymysql
import pymysql.cursors
from dotenv import load_dotenv
from flask import g

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))  # DB_HOST, DB_PASSWORD, ... from .env


def connect():
    """Open a new connection using the settings in .env."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "demandthread"),
        cursorclass=pymysql.cursors.DictCursor,  # rows come back as dictionaries
        autocommit=False,                        # nothing is saved until commit()
    )


def get_db():
    """Open the connection the first time it is needed in this request."""
    if "db" not in g:
        g.db = connect()
    return g.db


def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def query_all(sql, params=None):
    """SELECT many rows -> list of dictionaries."""
    with get_db().cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchall()


def query_one(sql, params=None):
    """SELECT the first row -> one dictionary (or None)."""
    with get_db().cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()


def execute(sql, params=None):
    """INSERT / UPDATE / DELETE: run it, commit, return the new row id."""
    db = get_db()
    with db.cursor() as cur:
        cur.execute(sql, params or ())
        new_id = cur.lastrowid
    db.commit()
    return new_id