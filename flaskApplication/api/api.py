from flask import Blueprint, render_template, request, jsonify
from flaskApplication.db import db
from flask import current_app
import ast
import sqlite3

api_bp = Blueprint('api_bp', __name__)

edit_selector_config = lambda \
        col: f'{{"title":"{col}", "field":"{col}", "editor":"select", "editorParams":{{"values":"true", "sortValuesList":"asc"}}}}'
edit_any_config = lambda col: f'{{"title":"{col}", "field":"{col}", "editor":"true"}}'
edit_date_config = lambda col: f'{{"title":"{col}", "field": "{col}", "editor":"dateEditor"}}'


@api_bp.route('/get_data/<table>')
def get_data(table):
    cols = ast.literal_eval(request.args.get('cols'))
    if len(cols) == 0:
        print('> Got json request for no data!')
        return '[]'
    print('> Got json request for data for columns:', cols, 'from table', table)
    query = f'select {", ".join(cols)} from {table}'
    try:
        result = db.query_db(current_app, query)
    except sqlite3.OperationalError as e:
        print('> Query caused error:', query)
        return '[]'
    data = [dict(row) for row in result]
    return jsonify(data)


@api_bp.route('/get_column_type/<table>')
def get_col_type(table):
    try:
        cols = dict(request.args)['cols[]']
    except KeyError:
        print('> Invalid request.')
        return '{}'
    print('> Got json request for column type of:', cols, 'from table', table)
    data = []
    for col in cols:
        if col == 'name':
            data.append(edit_selector_config(col))
        elif col == 'date':
            data.append(edit_date_config(col))
        else:
            data.append(edit_any_config(col))
    return jsonify(data)
