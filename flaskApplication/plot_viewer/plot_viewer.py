from flaskApplication.db import db
from flask import current_app
from flask import Blueprint, render_template, request, jsonify
import sqlite3
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json

plot_viewer_bp = Blueprint('plot_viewer_bp', __name__,
                           template_folder='templates',
                           static_folder='static',
                           static_url_path='/plot_viewer/static')


def create_plot(N):
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe

    data = [
        go.Bar(
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@plot_viewer_bp.route('/barchart')
def view_bar():
    return render_template('baseplot.html',
                           menu_items={'Transactions': '/view/transactions', 'Bar plot': '/plot/barchart'})


@plot_viewer_bp.route('/bar', methods=['GET', 'POST'])
def bar():
    N = int(request.args['N'])
    graphJSON = create_plot(N)
    return graphJSON
