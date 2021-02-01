from flask import Flask, render_template
import os
from flaskApplication.db import db
from flaskApplication.viewer.viewer import viewer_bp
from flaskApplication.api.api import api_bp
from flaskApplication.plot_viewer.plot_viewer import plot_viewer_bp

app = Flask(__name__, template_folder='C:\\Users\\mr\Documents\\Python Scripts\\Wie-betaald-wat\\templates')
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE='db/whopays.sqlite',
)

app.register_blueprint(viewer_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(plot_viewer_bp, url_prefix='/plot')

if __name__ == '__main__':
    db.init_db(app)
    db.init_app(app)
    app.run(debug=True)
