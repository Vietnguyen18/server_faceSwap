from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class Comment(db.Model):
    __tablename__ = 'comment'
    id_Comment = db.Column(db.Integer, primary_key=True)
    noi_dung_Comment  = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)
    IP_Comment  = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)
    device_Comment  = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)
    id_toan_bo_su_kien  = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)
    imageattach  = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)
    thoi_gian_release  = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_user = db.Column(db.Integer, nullable=True, default=None, unique=True)
    user_name = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, unique=True, default=None)
    avatar_user = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, unique=True, default=None)
    so_thu_tu_su_kien = db.Column(db.Integer, nullable=True, default=None)
    location = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)

    
