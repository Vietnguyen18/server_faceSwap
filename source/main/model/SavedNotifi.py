from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class SavedNotifi(db.Model):
    __tablename__ = 'saved_notification'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    id_user = db.Column(db.Integer, unique=True)
    id_toan_bo_su_kien = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    so_thu_tu_su_kien = db.Column(db.Integer, unique=True)
    user_name = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_avatar = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    link_imagesk = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    status = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    thoigian = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)

    



    
