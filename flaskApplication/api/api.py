from flask import Blueprint, render_template, request, jsonify
from flaskApplication.db import db
from flask import current_app
import ast
import sqlite3

api_bp = Blueprint('api_bp', __name__)

edit_selector_config = lambda \
        col: f'{{"title":"{col}", "field":"{col}", "editor":"select"}}'
edit_any_config = lambda col: f'{{"title":"{col}", "field":"{col}", "editor":"true", "formatter":"textarea"}}'
edit_date_config = lambda col: f'{{"title":"{col}", "field": "{col}", "editor":"dateEditor"}}'
mandatory_insert_cols = ['amount', 'date', 'what', 'name', 'attributed']


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


@api_bp.route('/del_data/<table>', methods=['POST'])
def del_data(table):
    data = ast.literal_eval(request.form['data'])
    query = f'''DELETE FROM {table} WHERE {' AND '.join([str(key) + ' == ' + str(data[key]) if type(data[key]) == float else str(key) + " == '" + str(data[key]) + "'" for key in data])}'''
    print(query)
    try:
        db.update_db(current_app, query)
    except sqlite3.OperationalError as e:
        print('> Query caused error:', query, e)
        return 'Delete failed!'
    else:
        return 'Delete successful!'


@api_bp.route('/post_data/<table>', methods=['POST'])
def post_data(table):
    data = request.form['data']
    query = f'select * from {table}'
    try:
        result = db.query_db(current_app, query)
        old = []
        for row in result:
            temp = dict(row)
            del temp['index']
            old.append(temp)
    except sqlite3.OperationalError as e:
        print('> Query caused error:', query)
        return 'Old data load failed!'
    else:
        new = ast.literal_eval(data.replace('null', 'None'))
        added = False
        for row in new:
            if row not in old:
                print(f'> Inserting new row into {table}: {row}')
                temp = {key: row[key] for key in row if row[key] is not None}
                if not all(i in temp.keys() for i in mandatory_insert_cols):
                    return 'Not all columns filled in!'
                query = f'''INSERT INTO {table} {str(tuple(temp.keys())).replace("'", '')}
                            VALUES {str(tuple(temp.values()))}'''
                try:
                    db.update_db(current_app, query)
                except sqlite3.OperationalError as e:
                    print('> Query caused error:', query)
                    print(e)
                    return f'Adding row {row} failed!'
                else:
                    added = True
        if added:
            return 'Added rows successfully!'
        else:
            return 'No new data found!'
