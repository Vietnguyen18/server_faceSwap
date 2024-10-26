from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class BlockUser(db.Model):
    __tablename__ = 'block_user'
    id_block = db.Column(db.Integer, primary_key=True, nullable=False)
    id_user_report = db.Column(db.Integer, nullable=False)
    id_blocked_user = db.Column(db.Integer, nullable=False)
    report_reason = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    status = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)



    
