from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class ListAlbum(db.Model):
    __tablename__ = 'listvideo_wedding'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    noidung = db.Column(db.String(1000,collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_album = db.Column(db.Integer, unique=True)
    server = db.Column(db.String(100,collation='utf8mb4_general_ci'), nullable=True, default=None) 
    linkThump = db.Column(db.String(200,collation='utf8mb4_general_ci'), nullable=True, default=None)

    



    
