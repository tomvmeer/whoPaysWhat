from flask import Blueprint, render_template
from flaskApplication.db import db
from flask import current_app
import sqlite3

viewer_bp = Blueprint('viewer_bp', __name__,
                      template_folder='templates',
                      static_folder='static'
                      , static_url_path='/viewer/static')


@viewer_bp.route('/view/<table>')
@viewer_bp.route('/view/<table>/<cols>')
def view_all(table, cols='*'):
    try:
        result = db.query_db(current_app, f'select {cols} from {table} limit(1)')
    except sqlite3.OperationalError as e:
        print(f'> Error causes by user at view_all:{e}.')
        return render_template('baseview.html', columns=[], table=table)
    cols = list(dict(result[0]).keys())
    if 'index' in cols:
        cols.remove('index')  # We don't need the index.
    return render_template('baseview.html', columns=cols, table=table,
                           menu_items={'Transactions': '/view/transactions', 'Bar plot': '/plot/barchart'})
