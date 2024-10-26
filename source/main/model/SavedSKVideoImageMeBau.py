from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class SavedSKVideoImageMeBau(db.Model):
    __tablename__ = 'saved_sukien_video_image_mebau'
    id_saved = db.Column(db.String(12,collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_video_goc = db.Column(db.String(100,collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_image = db.Column(db.String(100,collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_video_da_swap = db.Column(db.String(10000,collation='utf8mb4_general_ci'), nullable=True, default=None)
    thoigian_sukien = db.Column(db.String(20,collation='utf8mb4_general_ci'), nullable=True, default=None)
    device_them_su_kien = db.Column(db.String(20,collation='utf8mb4_general_ci'), nullable=True, default=None)
    ip_them_su_kien = db.Column(db.String(15,collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_user = db.Column(db.String(10,collation='utf8mb4_general_ci'), nullable=True, default=None)
    count_comment = db.Column(db.String(13,collation='utf8mb4_general_ci'), nullable=True, default=None)
    count_view = db.Column(db.String(10,collation='utf8mb4_general_ci'), nullable=True, default=None)
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    loai_sk = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)

