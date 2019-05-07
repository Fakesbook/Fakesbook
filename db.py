import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            check_same_thread=False
        )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource(current_app.config['DB_SCHEMA']) as f:
        db.executescript(f.read().decode('utf-8'))

def init_app(app):
    init_db()
    app.teardown_appcontext(close_db)
