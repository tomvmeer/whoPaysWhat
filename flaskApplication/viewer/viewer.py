from flask import Blueprint, render_template
from flaskApplication.db import db
from flask import current_app
import sqlite3

viewer_bp = Blueprint('viewer_bp', __name__,
                      template_folder='templates',
                      static_folder='static'
                      , static_url_path='/viewer/static')


@viewer_bp.route('/<table>')
def view_all(table):
    try:
        result = db.query_db(current_app, f'select * from {table} limit(1)')
    except sqlite3.OperationalError as e:
        print(f'> Error causes by user at view_all:{e}.')
        return render_template('base.html', columns=[], table=table)
    cols = list(dict(result[0]).keys())[1:]  # We don't need the index.
    return render_template('base.html', columns=cols, table=table)
