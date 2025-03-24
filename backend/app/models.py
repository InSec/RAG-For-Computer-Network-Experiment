from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    histories = db.relationship('History', back_populates='from_user', foreign_keys='History.from_user_id')


class History(db.Model):
    __tablename__ = 'history'
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    from_user = db.relationship('User', back_populates='histories', foreign_keys=[from_user_id])
    query = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)



