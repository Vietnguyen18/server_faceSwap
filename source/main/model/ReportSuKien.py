from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class ReportSuKien(db.Model):
    __tablename__ = 'report_sukien'
    id_toan_bo_su_kien = db.Column(db.Text(collation='utf8mb4_general_ci'), primary_key=True, nullable=True, default=None)
    so_thu_tu_su_kien = db.Column(db.Integer, unique=True, nullable=True, default=None)
    report_reason = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_user_report = db.Column(db.Integer,nullable=True, default=None)
    id_user_comment = db.Column(db.Integer,nullable=True, default=None)



    
