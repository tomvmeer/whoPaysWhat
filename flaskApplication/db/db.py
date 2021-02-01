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


def update_db(app, query):
    with app.app_context():
        conn = g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        print('> Closing db.')
        db.close()


def create_table(app, data, tablename):
    with app.app_context():
        db = get_db()
        df = pd.read_csv(f'db/{data}', index_col=0)
        try:
            df.to_sql(tablename, con=db, if_exists='fail', index=True)
        except sqlite3.OperationalError as e:
            print(f'> Error creating new table {tablename} from {data}.')
        else:
            print(f'> New table created successfully named {tablename} from {data}.')


def init_db(app):
    with app.app_context():
        db = get_db()
        print('> Initialising databases.')
        try:
            query_db(app, 'select * from transactions')
        except sqlite3.OperationalError as e:
            print('> Creating new database.', e)
            # Last database entry through csv: maren: 2020-11-11 00:00:00 tom: 2020-16-11.
            create_table(app, 'data.csv', 'transactions')