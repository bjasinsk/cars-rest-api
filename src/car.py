from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""
Car class representing the car model in the database    
"""


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    average_rate = db.Column(db.Float, default=0)
    vote_count = db.Column(db.Integer, default=0)

    __table_args__ = (db.UniqueConstraint('make', 'model', name='unique_make_model'),)
