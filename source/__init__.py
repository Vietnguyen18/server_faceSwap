import base64
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies
from flask_sslify import SSLify
import os

app = Flask(__name__)
CORS(app)
# sslify = SSLify(app)
app.config["SECRET_KEY"] = "devsenior"
app.config["SECURITY_PASSWORD_SALT"] = "devsenior"
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://sonpro:Ratiendi89@localhost/FutureLove4?charset=utf8mb4"
)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://sonpro:Ratiendi89@localhost:3306/FutureLove4?auth_plugin=mysql_native_password&charset=utf8mb4"
)
app.config["SQLAlCHEMY_TRACK_MODIFICATIONS"] = True
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "pxlphap@gmail.com"
app.config["MAIL_PASSWORD"] = "skouzcyupkkoheny"
app.config["POSTMARK_API"] = "71d6565b-6b12-4137-89e8-bd34439540c5"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

jwt = JWTManager(app)


connected_clients = []
app.app_context().push()
mail = Mail(app)
db = SQLAlchemy(app)
# socketIo = SocketIO(app, cors_allowed_origins="*")
# viet fix loi epoll 26 sep 2024
socketIo = SocketIO(
    app,
    cors_allowed_origins="*",
    max_http_buffer_size=1024 * 1024 * 50,
    logger=True,
    engineio_logger=True,
    async_mode="threading",
)
