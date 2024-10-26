from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class Users(db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, primary_key=True,autoincrement=True)
    link_avatar = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    user_name = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    ip_register = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    device_register = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    password = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    email = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    count_sukien = db.Column(db.Integer,nullable=True, default=None)
    count_comment = db.Column(db.Integer,nullable=True, default=None)
    count_view = db.Column(db.Integer,nullable=True, default=None)
    status = db.Column(db.Integer,nullable=True, default=1)
    type_register = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    time_create = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    time_coin_in_app = db.Column(db.Integer,nullable=True, default=0)

    
