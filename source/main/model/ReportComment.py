from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class ReportComment(db.Model):
    __tablename__ = 'report_comment'
    id_report = db.Column(db.Integer, primary_key=True,autoincrement=True)
    id_comment = db.Column(db.Integer, unique=True, nullable=True, default=None)
    report_reason = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    content = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    id_user_report = db.Column(db.Integer,nullable=True, default=None)
    id_user_comment = db.Column(db.Integer,nullable=True, default=None)

    



    
