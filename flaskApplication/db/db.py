import sqlite3
import pandas as pd
import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
    app.teardown_appcontext(close_db)


def get_db():
    if 'db' not in g:
        print('> Opening database connection.')
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def query_db(app, query, args=(), one=False):
    with app.app_context():
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        print('> Closing db.')
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()
        print('> Initialising database.')
        try:
            query_db(app, 'select * from transactions')
        except sqlite3.OperationalError as e:
            print('> Creating new database.', e)
            df = pd.read_csv('db/data.csv', index_col=0)
            # Last database entry through csv: maren: 2020-11-11 00:00:00 tom: 2020-16-11.
            df.to_sql('transactions', con=db, if_exists='replace', index=True)
