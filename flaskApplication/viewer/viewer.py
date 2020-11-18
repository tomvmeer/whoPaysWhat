from flask import Blueprint, render_template
from flaskApplication.db import db
from flask import current_app

viewer_bp = Blueprint('viewer_bp', __name__,
                      template_folder='templates',
                      static_folder='static'
                      , static_url_path='/viewer/static')

edit_selector_config = lambda \
        col: "{'title': '" + col + "', 'field': '" + col + "', 'editor': 'select', 'editorParams': {'values': true, 'sortValuesList': 'asc'}}"
edit_any_config = lambda col: "{'title': '" + col + "', 'field': '" + col + "', 'editor': true}"
edit_date_config = lambda col: "{'title': '" + col + "', 'field': '" + col + "', 'editor': dateEditor}"


@viewer_bp.route('/')
def view_all():
    result = db.query_db(current_app, 'select * from transactions')
    data = [dict(row) for row in result]
    columns = []
    for col in data[0]:
        if col == 'name':
            columns.append(edit_selector_config(col))
        elif col == 'date':
            columns.append(edit_date_config(col))
        else:
            columns.append(edit_any_config(col))

    return render_template('table-generator.html', table_data=data, table_columns=columns[:-2])
