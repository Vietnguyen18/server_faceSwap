from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class DeviceTokenIos(db.Model):
    __tablename__ = 'device_token_ios'
    id_user = db.Column(db.Integer, primary_key=True, unique=True)
    device_name = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)
    device_token = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)


    
