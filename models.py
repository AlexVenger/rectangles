from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Rectangle(db.Model):
    __tablename__ = 'rectangles'
    rectangle_id = db.Column(db.Integer, primary_key=True)
    x1 = db.Column(db.Float, nullable=False)
    y1 = db.Column(db.Float, nullable=False)
    x2 = db.Column(db.Float, nullable=False)
    y2 = db.Column(db.Float, nullable=False)
    x3 = db.Column(db.Float, nullable=False)
    y3 = db.Column(db.Float, nullable=False)
    x4 = db.Column(db.Float, nullable=False)
    y4 = db.Column(db.Float, nullable=False)
