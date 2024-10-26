from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class CategoriesVideo(db.Model):
    __tablename__ = 'categories_video'
    idCateogries = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nameCategories = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False, default=None)
    detail = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False, default=None)

    
