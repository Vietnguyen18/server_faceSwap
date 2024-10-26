from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class GmailFrom(db.Model):
    __tablename__ = 'gmail_from'
    id_user = db.Column(db.Integer, primary_key=True,autoincrement=True)
    gmail = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)
    password = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)
    password_app = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=False)


    
