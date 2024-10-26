from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class ListImageAlone(db.Model):
    __tablename__ = 'listImage_alone'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    mask = db.Column(db.String(100,collation='utf8mb4_general_ci'), nullable=True, default=None)
    thongtin = db.Column(db.String(100,collation='utf8mb4_general_ci'), nullable=True, default=None)
    image = db.Column(db.String(1000,collation='utf8mb4_general_ci'), nullable=True, default=None)
    dotuoi = db.Column(db.String(100,collation='utf8mb4_general_ci'), nullable=True, default=None)
    IDCategories = db.Column(db.Integer, primary_key=True)


    
