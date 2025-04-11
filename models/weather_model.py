from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    __tablename__ = "weather_data"  # ✅ Explicitly define table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=True)
    weather = db.Column(db.String(100), nullable=True)
