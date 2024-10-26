from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from source import db


class WeddingDetail(db.Model):
    __tablename__ = 'wedding_details'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    groom_name = db.Column(db.String(255,collation='utf8mb4_general_ci'), nullable=True, default=None)
    bride_name = db.Column(db.String(255,collation='utf8mb4_general_ci'), nullable=True, default=None)
    wedding_date = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    wedding_image = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    wedding_location = db.Column(db.String(255,collation='utf8mb4_general_ci'), nullable=True, default=None)
    google_maps_link = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    qr_code_image = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    attendance_status = db.Column(db.Enum('going', 'not going', 'not going but sending', name='attendance_status'),
        nullable=False,
        default=None,)
    id_user = db.Column(db.Integer, nullable=True, default=None)
    groom_image = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)
    bride_image = db.Column(db.Text(collation='utf8mb4_general_ci'), nullable=True, default=None)


    
