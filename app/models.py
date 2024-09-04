# app/models.py

from .db import db
import datetime

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False)
    client_ip = db.Column(db.String(45), nullable=False)
    created_time = db.Column(db.Integer, default=int(datetime.datetime.utcnow().timestamp()))
    addresses = db.relationship('Address', backref='query', lazy=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(45), nullable=False)
    query_id = db.Column(db.Integer, db.ForeignKey('query.id'), nullable=False)
