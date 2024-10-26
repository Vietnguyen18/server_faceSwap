from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class ListVideo(db.Model):
    __tablename__ = 'listVideo'
    IDCategories = db.Column(db.Integer,nullable=True,default=None)
    age_video = db.Column(db.Integer, nullable=True,default=None)
    chung_toc = db.Column(db.String(6,collation='utf8mb4_general_ci'), nullable=True, default=None)
    gioitinh = db.Column(db.String(6,collation='utf8mb4_general_ci'), nullable=True, default=None)
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    linkgoc = db.Column(db.String(120,collation='utf8mb4_general_ci'), nullable=True, default=None)
    mau_da = db.Column(db.String(5,collation='utf8mb4_general_ci'), nullable=True, default=None)
    noidung = db.Column(db.String(24,collation='utf8mb4_general_ci'), nullable=True, default=None)
    numberUsed = db.Column(db.Boolean, nullable=False, default=None) 
    thumbnail = db.Column(db.String(104,collation='utf8mb4_general_ci'), nullable=True, default=None)

    



    
