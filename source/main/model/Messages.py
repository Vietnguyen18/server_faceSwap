from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class Messages(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    receiver_id = db.Column(db.Integer, unique=True, nullable=True, default=None)
    sender_id = db.Column(db.Integer, unique=True,nullable=True, default=None)
    message = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    contact_id = db.Column(db.Integer, unique=True,nullable=True, default=None)

    



    
