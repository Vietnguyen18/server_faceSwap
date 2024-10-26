from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class AddSuKien(db.Model):
    __tablename__ = 'add_sukien'
    id_add = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_toan_bo_su_kien = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = False)
    ten_sukien = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = False)
    noidung_su_kien = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = False)
    ten_nam = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = True)
    ten_nu = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = True, default=None)
    device_them_su_kien = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = True, default = None)
    ip_them_su_kien = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = True, default = None)
    link_img = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = True, default = None)
    link_video = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = True, default = None)
    id_template = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = True, default = None)
    thoigian_themsk = db.Column(db.Text(collation = 'utf8mb4_general_ci'), nullable = True, default = None)
    so_thu_tu_su_kien = db.Column(db.Integer, nullable = True, default = None)
    count_comment= db.Column(db.Integer, nullable = True, default = None)
    count_view= db.Column(db.Integer, nullable = True, default = None)
    status= db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable = True, default = None)


    
