from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class ListVideoCatwalk(db.Model):
    __tablename__ = 'listVideo_Catwalk'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    linkgoc = db.Column(db.String(2320,collation='utf8mb4_general_ci'), nullable=True, default=None)
    noidung = db.Column(db.String(110,collation='utf8mb4_general_ci'), nullable=True, default=None)
    thumbnail = db.Column(db.String(242,collation='utf8mb4_general_ci'), nullable=True, default=None)
    numberUsed = db.Column(db.Boolean, nullable=False, default=None)
    IDCategories = db.Column(db.String(12,collation='utf8mb4_general_ci'), nullable=True, default=None)
    age_video = db.Column(db.String(9,collation='utf8mb4_general_ci'), nullable=True, default=None)
    gioitinh = db.Column(db.String(15,collation='utf8mb4_general_ci'), nullable=True, default=None)
    mau_da = db.Column(db.String(6,collation='utf8mb4_general_ci'), nullable=True, default=None)
    chung_toc = db.Column(db.String(9,collation='utf8mb4_general_ci'), nullable=True, default=None)

    



    
