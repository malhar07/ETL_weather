import os
from flask import Flask, render_template, request
from sqlalchemy import inspect
from models.weather_model import db, WeatherData
from controllers.bulk_controller import bulk_bp  # ✅ Keeps bulk insert
from controllers.etl_controller import etl_bp  # ✅ Adds ETL processing

import logging
app = Flask(__name__, static_folder='static', template_folder='templates')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "weather_data.db")
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table("weather_data"):
        print("⚡ Table does NOT exist. Creating now...")
        db.create_all()
        print("✅ Database and table created!")
    else:
        print("✅ Table already exists!")

# ✅ Keeping original functionalities
app.register_blueprint(bulk_bp, url_prefix="/bulk")
app.register_blueprint(etl_bp, url_prefix="/etl")  # ✅ Adds ETL blueprint

@app.route('/')
def home():
    try:
        page = int(request.args.get('page', 1))
        per_page = 10
        paginated_data = WeatherData.query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('index.html', data=paginated_data)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port = 8080)
