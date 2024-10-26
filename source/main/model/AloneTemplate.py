from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class AloneTemplate(db.Model):
    __tablename__ = 'alone_template'
    id_cate = db.Column(db.Integer, primary_key=True, nullable=False)
    name_cate = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    number_image = db.Column(db.Integer, nullable=False)
    folder_name = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    selected_swap = db.Column(db.Integer, nullable=False)
    image_sample = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)




    
