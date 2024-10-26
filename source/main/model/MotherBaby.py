from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class MotherBaby(db.Model):
    __tablename__ = 'Mother_baby'
    id_cate = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name_cate = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    number_image = db.Column(db.Integer,nullable=True, default=None)
    folder_name = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    selected_swap = db.Column(db.Integer,nullable=True, default=None)
    image_sample = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)

    



    
