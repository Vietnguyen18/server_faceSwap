from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class SavedSKVideoImageWedding(db.Model):
    __tablename__ = 'saved_sukien_video_image_wedding'
    id_saved = db.Column(db.String(12,collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_video_goc = db.Column(db.String(1000,collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_image = db.Column(db.String(1000,collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_video_da_swap = db.Column(db.String(10000,collation='utf8mb4_general_ci'), nullable=True, default=None)
    thoigian_sukien = db.Column(db.String(50,collation='utf8mb4_general_ci'), nullable=True, default=None)
    device_them_su_kien = db.Column(db.String(50,collation='utf8mb4_general_ci'), nullable=True, default=None)
    ip_them_su_kien = db.Column(db.String(50,collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_user = db.Column(db.String(1000,collation='utf8mb4_general_ci'), nullable=True, default=None)
    count_comment = db.Column(db.String(1000,collation='utf8mb4_general_ci'), nullable=True, default=None)
    count_view = db.Column(db.String(1000,collation='utf8mb4_general_ci'), nullable=True, default=None)
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)


    



    
