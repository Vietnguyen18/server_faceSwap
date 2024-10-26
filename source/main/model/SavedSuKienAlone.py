from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class SavedSuKienAlone(db.Model):
    __tablename__ = 'saved_sukien_alone'
    id_saved = db.Column(db.Text(collation='utf8mb4_general_ci'),primary_key=True, nullable=True, default=None)
    link_src_goc = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_da_swap = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_toan_bo_su_kien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    thoigian_sukien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    device_them_su_kien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    ip_them_su_kien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_user = db.Column(db.Integer, unique=True)
    count_comment = db.Column(db.Integer,nullable=True, default=None )
    count_view = db.Column(db.Integer,nullable=True, default=None )
    id_template = db.Column(db.Integer,nullable=True, default=None )
    loai_sukien = db.Column(db.String(100,collation='utf8mb4_general_ci'), nullable=True, default=None)
    album = db.Column(db.String(100,collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_sk_album = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)


    



    
