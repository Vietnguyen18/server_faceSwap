from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class SavedSuKienVideo(db.Model):
    __tablename__ = 'saved_sukien_video'
    id_saved = db.Column(db.Text(collation='utf8mb4_general_ci'),primary_key=True, nullable=True, default=None)
    link_video = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_image = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_da_swap = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    ten_su_kien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    noidung_su_kien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_video = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    thoigian_sukien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    device_them_su_kien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    ip_them_su_kien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_user = db.Column(db.Integer, unique=True)
    count_comment = db.Column(db.Integer,nullable=True, default=None )
    count_view = db.Column(db.Integer,nullable=True, default=None )
    link_video_goc = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    thoigian_swap = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)


    



    
