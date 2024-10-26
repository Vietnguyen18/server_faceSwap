from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class SavedImage(db.Model):
    __tablename__ = 'save_image'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    id_user = db.Column(db.Integer, unique=True)
    link_image = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    thoigian = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)

    



    
