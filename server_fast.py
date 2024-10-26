import math
from fastapi import FastAPI, Query, Request, APIRouter, Form, HTTPException
import re
from PIL import Image
from io import BytesIO
from flask import jsonify
from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydantic import BaseModel, EmailStr
import cv2
from email.message import EmailMessage
import face_recognition
from source.main.function.roop.face_analyser import get_one_face
from source.sendmail import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import zipfile
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from source import db

from source.sendmail import (
    save_user_to_mysql,
    send_mail,
    generate_token,
    verify_password,
    send_mail_reset,
    validate_token,
    send_mail_notifi,
    send_mail_del_account,
)
import jwt
import pytz
from typing import Optional
from datetime import datetime
import uuid
from pydantic import BaseModel
from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from typing import List
import os, random, base64, shutil
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth
from postmarker.core import PostmarkClient
from sqlalchemy import func, desc, not_, or_

# model
from source.main.model.AddSuKien import AddSuKien
from source.main.model.BlockUser import BlockUser
from source.main.model.CategoriesVideo import CategoriesVideo
from source.main.model.Comment import Comment
from source.main.model.DeviceTokenIos import DeviceTokenIos
from source.main.model.GmailFrom import GmailFrom
from source.main.model.ListAlbum import ListAlbum
from source.main.model.ListImageAlone import ListImageAlone
from source.main.model.ListImageBaby import ListImageBaby
from source.main.model.ListImageBikini import ListImageBikini
from source.main.model.ListImageFancyAI import ListImageFancyAI
from source.main.model.ListImageMotherBaby import ListImageMotherBaby
from source.main.model.ListImagePreg import ListImagePreg
from source.main.model.ListImageSanta import ListImageSanta
from source.main.model.ListImageWedding import ListImageWedding
from source.main.model.ListVideo import ListVideo
from source.main.model.ListVideoAnime import ListVideoAnime
from source.main.model.ListVideoBaby import ListVideoBaby
from source.main.model.ListVideoBabyfunny import ListVideoBabyFunny
from source.main.model.ListVideoBabyFuture import ListVideoBabyFuture
from source.main.model.ListVideoCatwalk import ListVideoCatwalk
from source.main.model.ListVideoHallowen import ListVideoHallowen
from source.main.model.ListVideoMebau import ListVideoMebau
from source.main.model.ListVideoModel import ListVideoModel
from source.main.model.ListVideoSanta import ListVideoSanta
from source.main.model.ListVideoSantaNew import ListVideoSantaNew
from source.main.model.ListVideoWedding import ListVideoWedding
from source.main.model.Messages import Messages
from source.main.model.MotherBaby import MotherBaby
from source.main.model.ReportComment import ReportComment
from source.main.model.ReportSuKien import ReportSuKien
from source.main.model.SavedImage import SavedImage
from source.main.model.SavedNotifi import SavedNotifi
from source.main.model.SavedSKVideoImageGrowup import SavedSKVideoImageGrowup
from source.main.model.SavedSKVideoImageMeBau import SavedSKVideoImageMeBau
from source.main.model.SavedSKVideoImageWedding import SavedSKVideoImageWedding
from source.main.model.SavedSKVideoSwapImage import SavedSKVideoSwapImage
from source.main.model.SavedSuKien import SavedSuKien
from source.main.model.SavedSuKien2Img import SavedSuKien2Img
from source.main.model.SavedSuKienAlone import SavedSuKienAlone
from source.main.model.SavedSuKienSwapBaby import SavedSuKienSwapBaby
from source.main.model.SavedSuKienVideo import SavedSuKienVideo
from source.main.model.Users import Users
from source.main.model.VideoWedding import VideoWedding
from source.main.model.WeddingDetail import WeddingDetail

client = PostmarkClient(server_token="2c787e55-cd01-48d8-866a-f2915547adbf")


# pip install insightface==0.2.1 onnxruntime moviepy
# app = FastAPI()
# app = FastAPI()
router = APIRouter()

origins = ["*"]
secret_key = "wefhoiwfhsfiug9034bfjkg47vdjk"  # token key
ALGORITHM = "HS256"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # SessionMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="!secret")


# Initialize our OAuth instance from the client ID and client secret specified in our .env file
config1 = Config(".env")
oauth = OAuth(config1)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)


@app.get("/", tags=["authentication"])
async def home(request: Request):
    user = request.session.get("user")
    print(user)
    if user is not None:
        thong_tin = {}
        try:
            user_info = Users.query.filter(Users.email == user["email"]).filter()
            if user_info:
                thong_tin["id_user"] = (user_info.id_user,)
                thong_tin["link_avatar"] = (user_info.link_avatar,)
                thong_tin["user_name"] = (user_info.user_name,)
                thong_tin["ip_register"] = (user_info.ip_register,)
                thong_tin["device_register"] = (user_info.device_register,)
                thong_tin["email"] = (user_info.email,)
                thong_tin["count_sukien"] = (user_info.count_sukien,)
                thong_tin["count_comment"] = (user_info.count_comment,)
                thong_tin["count_view"] = (user_info.count_view,)
                thong_tin["type"] = (user_info.type_register,)
                token = (generate_token(user_info.user_name),)
                thong_tin["token"] = token
                return thong_tin
            else:
                new_user = Users(
                    email=user["email"],
                    user_name=user["name"],
                    link_avatar=user["link_avatar"],
                    ip_register="device",
                    device_register="google",
                    count_sukien=0,
                    count_comment=0,
                    count_view=0,
                    type_register="user",
                )
                db.session.add(new_user)
                db.session.commit()
                db.session.refresh(new_user)
                # get lai thong tin
                thong_tin["id_user"] = (user_info.id_user,)
                thong_tin["link_avatar"] = (user_info.link_avatar,)
                thong_tin["user_name"] = (user_info.user_name,)
                thong_tin["ip_register"] = (user_info.ip_register,)
                thong_tin["device_register"] = (user_info.device_register,)
                thong_tin["email"] = (user_info.email,)
                thong_tin["count_sukien"] = (user_info.count_sukien,)
                thong_tin["count_comment"] = (user_info.count_comment,)
                thong_tin["count_view"] = (user_info.count_view,)
                thong_tin["type"] = (user_info.type_register,)
                token = (generate_token(user_info.user_name),)
                thong_tin["token"] = token
                return thong_tin
        except Exception as error:
            db.session.rollback()
            return f"Failed -----------: {error}"
        finally:
            db.session.close()
    return HTMLResponse('<a href="/login/user">login</a>')


from starlette.datastructures import URL


@app.get(
    "/login/user", tags=["authentication"]
)  # Tag it as "authentication" for our docs
async def login_user(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for("auth")
    print(type(redirect_uri))
    print(redirect_uri)
    redirect_uri = redirect_uri.replace(scheme="https")
    print(redirect_uri)
    print(type(redirect_uri))
    # redirect_uri = 'https://metatechvn.store/auth'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route("/auth")
async def auth(request: Request):
    # Perform Google OAuth
    token = await oauth.google.authorize_access_token(request)
    # user = await oauth.google.parse_id_token(request, token)
    # Save the user
    request.session["user"] = token["userinfo"]
    return RedirectResponse(url="/")


@app.get("/logout", tags=["authentication"])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop("user", None)

    return RedirectResponse(url="/")


@app.get("/list_category", tags=["list data"])
async def get_list_category():
    list_category = []
    try:
        result = CategoriesVideo.query.all()
        for item in result:
            data = {}
            data["id"] = item[0]
            data["name"] = item[1]
            data["detail"] = item[2]
            list_category.append(data)

        return list_category
    except Exception as error:
        db.session.rollback()
        print(f"Failed---------- : {error}")


@app.get("/lovehistory/sukien/video/{id_su_kien_video}")
async def get_data_love_history(id_su_kien_video: str):
    thong_tin = {}
    list_thong_tin = []
    base_url = "https://photo.gachmen.org/image/video_sk"
    try:
        result2 = SavedSuKienVideo.query.filter(
            SavedSuKienVideo.id_saved == id_su_kien_video
        )
        print("---result2-----", str(result2))
        for i in range(0, len(result2)):
            id_category = (
                db.session.query(ListVideo.IDCategories)
                .filter(ListVideo.id == i.id_video)
                .scalar()
            )
            category_detail = CategoriesVideo.query.filter(
                CategoriesVideo.idCateogries == id_category
            ).first()
            thong_tin["id_video"] = (i.id_saved,)
            thong_tin["link_image"] = (i.link_image,)
            thong_tin["link_vid_swap"] = (i.link_da_swap,)
            thong_tin["link_video_goc"] = (i.link_video_goc,)
            thong_tin["thoigian_swap"] = (i.thoigian_swap,)
            thong_tin["id_categories"] = (id_category.IDCategories,)
            thong_tin["name_categories"] = (category_detail.nameCategories,)
            thong_tin["detail"] = (category_detail.detail,)
            thong_tin["ten_su_kien"] = (i.ten_su_kien,)
            thong_tin["noidung_sukien"] = (i.noidung_su_kien,)
            thong_tin["id_video_swap"] = (i.id_video,)
            thong_tin["thoigian_taosk"] = (i.thoigian_sukien,)
            thong_tin["id_user"] = (i.id_user,)
            thong_tin["count_comment"] = (i.count_comment,)
            thong_tin["count_view"] = (id.count_view,)
            list_thong_tin.append(thong_tin)

        print("data-------", list_thong_tin)
        return JSONResponse(content={"sukien_video": list_thong_tin, "status": 200})

    except Exception as error:
        db.session.rollback()
        print(f"----loi roi---------: {error}")
        return {"status": 500, "message": f"Error: {error}"}


@app.get("/images/{id_user}")
def get_image_links(request: Request, id_user: int):
    type = request.query_params.get("type")
    image_links = []
    folder_path_nam = f"/var/www/build_futurelove/image/image_user/{id_user}/nam"
    folder_path_video = f"/var/www/build_futurelove/image/image_user/{id_user}/video"
    folder_path_nu = f"/var/www/build_futurelove/image/image_user/{id_user}/nu"
    base_url = "https://photo.gachmen.org"
    if type == "nam":
        if os.path.isdir(folder_path_nam):
            for filename in os.listdir(folder_path_nam):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_nam, filename)
                    image_links.append(image_path)
        updated_links = [
            link.replace("/var/www/build_futurelove", base_url) for link in image_links
        ]
        return {"image_links_nam": updated_links}

    if type == "nu":
        if os.path.isdir(folder_path_nu):
            for filename in os.listdir(folder_path_nu):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_nu, filename)
                    image_links.append(image_path)
        updated_links = [
            link.replace("/var/www/build_futurelove", base_url) for link in image_links
        ]
        return {"image_links_nu": updated_links}

    if type == "video":
        if os.path.isdir(folder_path_video):
            for filename in os.listdir(folder_path_video):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_video, filename)
                    image_links.append(image_path)
        if os.path.isdir(folder_path_nam):
            for filename in os.listdir(folder_path_nam):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_nam, filename)
                    image_links.append(image_path)

        if os.path.isdir(folder_path_nu):
            for filename in os.listdir(folder_path_nu):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path_nu, filename)
                    image_links.append(image_path)
        updated_links = [
            link.replace("/var/www/build_futurelove", base_url) for link in image_links
        ]
        return {"image_links_video": updated_links}


@app.get("/lovehistory/listvideo/{page}")
async def get_data_list_video(request: Request, page: int):
    category = request.query_params.get("category")
    result = dict()
    try:
        limit = 50
        offset = (page - 1) * limit
        total_page = 0
        data_fet = ""

        if category == "0":
            count_category = ListVideo.query.count()
            total_page = math.ceil(count_category / limit)
            data_fet = ListVideo.query.limit(limit).offset(offset).all()

        elif category != "0":
            data_fet = (
                ListVideo.query.filter(ListVideo.IDCategories == category)
                .limit(limit)
                .offset(offset)
                .all()
            )
            data_length = len(data_fet)
            total_page = math.ceil(data_length / limit)

        list_video = []
        if page <= total_page:
            for item in data_fet:
                data = {}
                result3 = CategoriesVideo.query.filter(
                    CategoriesVideo.idCateogries == item.IDCategories
                ).first()
                number_of_rows = len(result3)
                if number_of_rows != 0:
                    data["name_categories"] = (result3.nameCategories,)
                    data["detail"] = (result3.detail,)
                else:
                    data["name_categories"] = ("No name categories",)
                    data["detail"] = ("No categories",)
                data["id"] = (item.id,)
                data["link_video"] = (item.linkgoc,)
                data["age_video"] = (item.age_video,)
                data["chung_toc"] = (item.chung_toc,)
                data["gioi_tinh"] = (item.gioitinh,)
                data["id_categories"] = (item.IDCategories,)
                data["mau_da"] = (item.mau_da,)
                data["noi_dung"] = (item.noidung,)
                data["thumbnail"] = item.thumbnail
                list_video.append(data)
        else:
            return JSONResponse(content="exceed the number of pages!!!")

        result["list_video"] = list_video
        result["total_page"] = total_page
        return JSONResponse(content=result)

    except Exception as e:
        db.session.rollback()
        print(e)
        return f"Request failed: {e}"


@app.get("/lovehistory/{idlove}")
async def get_data_love_history(idlove: str):
    thong_tin = {}
    list_thong_tin = []
    try:
        result2 = SavedSuKien.query.filter(
            SavedSuKien.id_toan_bo_su_kien == idlove
        ).all()

        for i in range(0, result2):
            thong_tin["id"] = (i.id_saved,)
            thong_tin["link_nam_goc"] = (i.link_nam_goc,)
            thong_tin["link_nu_goc"] = (i.link_nu_goc,)
            thong_tin["link_nam_chua_swap"] = (i.link_nam_chua_swap,)
            thong_tin["link_nu_chua_swap"] = (i.link_nu_chua_swap,)
            thong_tin["link_da_swap"] = (i.link_da_swap,)
            thong_tin["real_time"] = (i.thoigian_swap,)
            thong_tin["tom_luoc_text"] = (i.tomLuocText,)
            thong_tin["noi_dung_su_kien"] = (i.noidung_su_kien,)
            thong_tin["ten_su_kien"] = (i.ten_su_kien,)
            thong_tin["so_thu_tu_su_kien"] = (i.so_thu_tu_su_kien,)
            thong_tin["id_user"] = (i.id_user,)
            thong_tin["phantram_loading"] = (i.phantram_loading,)
            thong_tin["count_comment"] = (i.count_comment,)
            thong_tin["count_view"] = (i.count_view,)
            thong_tin["ten_nam"] = (i.ten_nam,)
            thong_tin["ten_nu"] = (i.ten_nu,)
            thong_tin["id_template"] = (i.id_template,)
            id_user = i.id_user
            name = Users.query.filter_by(id_user=id_user).first()
            if name == None:
                name = "Anonymous people"
            else:
                name = name.user_name
            thong_tin["user_name_tao_sk"] = name
            list_thong_tin.append(thong_tin)

        print("-----data------", list_thong_tin)
        return JSONResponse(content={"sukien": list_thong_tin})

    except Exception as error:
        db.session.rollback()
        print(f"Failed------------: {error}")


@app.get("/lovehistory/video/{page}")
async def get_data_video(page: int):
    list_toan_bo_sukien_saved = []
    try:
        result = (
            db.session.query(
                SavedSuKienVideo.id_saved, func.max(SavedSuKienVideo.thoigian_sukien)
            )
            .group_by(SavedSuKienVideo.id_saved)
            .order_by(SavedSuKienVideo.max_thoigian_swap.desc())
            .all()
        )
        records = []
        for row in result:
            id_toan_bo_su_kien = row.id_saved
            records.append(id_toan_bo_su_kien)

        soPhanTuTrenMotTrang = 8
        soTrang = (len(records) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang

        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(records))
        else:
            return JSONResponse(content="exceed the number of pages!!!")

        for i in range(start, end):
            idItemPhanTu = records[i]
            Mot_LanQuerryData = []
            print("idItemPhanTu ____ " + str(idItemPhanTu))
            thong_tin = {}
            phantupro = SavedSuKienVideo.query.filter(
                SavedSuKienVideo.id_saved == idItemPhanTu
            ).all()
            for i in range(0, phantupro):
                thong_tin["id_video"] = (i.id_saved,)
                thong_tin["link_image"] = (i.link_image,)
                thong_tin["link_vid_swap"] = (i.link_da_swap,)
                thong_tin["link_video_goc"] = (i.link_video_goc,)
                thong_tin["thoigian_swap"] = (i.thoigian_swap,)
                thong_tin["ten_su_kien"] = (i.ten_su_kien,)
                thong_tin["noidung_sukien"] = (i.noidung_su_kien,)
                thong_tin["id_video_swap"] = (i.id_video,)
                thong_tin["thoigian_taosk"] = (i.thoigian_sukien,)
                thong_tin["id_user"] = (i.id_user,)
                thong_tin["count_comment"] = (i.count_comment,)
                thong_tin["count_view"] = i.count_view
                Mot_LanQuerryData.append(thong_tin)
                thong_tin = {}

            list_toan_bo_sukien_saved.append({"sukien_video": Mot_LanQuerryData})

        return JSONResponse(content={"list_sukien_video": list_toan_bo_sukien_saved})
    except Exception as error:
        db.session.rollback()
        print(f"Failed---------------: {error}")
        return {f" Error Exception: {error}"}


@app.get("/lovehistory/user/video/{id_user}")
async def get_data_video_user(request: Request, id_user: int, page: int):
    page = request.query_params.get("page")
    page = int(page)
    print("___ID_USEER " + str(id_user) + " TRANG " + str(page))
    list_toan_bo_sukien_saved = []
    try:
        result = (
            db.session.query(
                SavedSuKienVideo.id_saved, func.max(SavedSuKienVideo.thoigian_sukien)
            )
            .filter(SavedSuKienVideo.id_user == id_user)
            .group_by(SavedSuKienVideo.id_saved)
            .order_by(SavedSuKienVideo.max_thoigian_swap.desc())
            .all()
        )
        records = []
        for row in result:
            id_toan_bo_su_kien = row.id_saved
            records.append(id_toan_bo_su_kien)

        soPhanTuTrenMotTrang = 8
        soTrang = (len(records) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang

        start = 0
        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(records))
        else:
            return JSONResponse(content="exceed the number of pages!!!")
        print(start)
        print("soTrang " + str(soTrang))
        for i in range(start, end):
            idItemPhanTu = records[i]
            Mot_LanQuerryData = []
            thong_tin = {}
            phantupro = SavedSuKienVideo.query.filter(
                SavedSuKienVideo.id_saved == idItemPhanTu
            ).all()
            for i in range(0, phantupro):
                thong_tin["id_video"] = (i.id_saved,)
                thong_tin["link_image"] = (i.link_image,)
                thong_tin["link_vid_swap"] = (i.link_da_swap,)
                thong_tin["link_video_goc"] = (i.link_video_goc,)
                thong_tin["thoigian_swap"] = (i.thoigian_swap,)
                thong_tin["ten_su_kien"] = (i.ten_su_kien,)
                thong_tin["noidung_sukien"] = (i.noidung_su_kien,)
                thong_tin["id_video_swap"] = (i.id_video,)
                thong_tin["thoigian_taosk"] = (i.thoigian_sukien,)
                thong_tin["id_user"] = (i.id_user,)
                thong_tin["count_comment"] = (i.count_comment,)
                thong_tin["count_view"] = i.count_view
                print("thongtin " + str(thong_tin))
                Mot_LanQuerryData.append(thong_tin)
                thong_tin = {}

            list_toan_bo_sukien_saved.append({"sukien_video": Mot_LanQuerryData})

        return JSONResponse(content={"list_sukien_video": list_toan_bo_sukien_saved})
    except Exception as error:
        db.session.rollback()
        return f"Failed-------------: {error}"


# create comment
@app.post("/lovehistory/comment")
async def create_comment(request: Request):
    form_data = await request.form()
    noi_dung_cmt = form_data.get("noi_dung_cmt")
    device_cmt = form_data.get("device_cmt")
    id_toan_bo_su_kien = form_data.get("id_toan_bo_su_kien")
    so_thu_tu_su_kien = form_data.get("so_thu_tu_su_kien")
    ipComment = form_data.get("ipComment")
    imageattach = form_data.get("imageattach")
    id_user = form_data.get("id_user")
    id_user_comment = form_data.get("id_user_cmt")
    location = form_data.get("location")
    link_imagesk = form_data.get("link_imagesk")
    if imageattach is None:
        imageattach = ""
    if id_user:
        id_user = id_user
    else:
        id_user = 0

    thong_tin = {}
    try:
        ketqua = Comment.query.with_entities(func.max(Comment.id_Comment)).scalar()

        if ketqua:
            id_comment = ketqua.id_Comment + 1
        else:
            id_comment = 1

        dt_utc = datetime.now()
        tz = pytz.timezone("Asia/Bangkok")
        dt_local = dt_utc.astimezone(tz)
        datetimenow = dt_local.strftime("%Y-%m-%d %H:%M:%S")
        ketqua_user = Users.query.filter(Users.id_user == id_user).filter()
        saved_sukien = SavedSuKien.query.filter(
            SavedSuKien.id_toan_bo_su_kien == id_toan_bo_su_kien
        ).all()

        thong_tin["device_cmt"] = device_cmt
        thong_tin["dia_chi_ip"] = ipComment
        thong_tin["id_comment"] = id_comment
        thong_tin["id_toan_bo_su_kien"] = id_toan_bo_su_kien
        thong_tin["so_thu_tu_su_kien"] = int(so_thu_tu_su_kien)
        thong_tin["imageattach"] = imageattach
        thong_tin["link_nam_goc"] = saved_sukien.link_nam_goc
        thong_tin["link_nu_goc"] = saved_sukien.link_nu_goc
        thong_tin["noi_dung_cmt"] = noi_dung_cmt
        thong_tin["thoi_gian_release"] = datetimenow
        thong_tin["location"] = location
        thong_tin["user_name"] = "Guest"
        thong_tin["avatar_user"] = None
        thong_tin["id_user"] = int(id_user)
        if ketqua_user:
            thong_tin["user_name"] = ketqua_user.user_name
            thong_tin["avatar_user"] = ketqua_user.link_avatar
        # Trả về thông báo thành công nếu comment được chèn thành công
        new_comment = Comment(
            id_Comment=id_comment,
            noi_dung_Comment=noi_dung_cmt,
            IP_Comment=ipComment,
            device_Comment=device_cmt,
            id_toan_bo_su_kien=id_toan_bo_su_kien,
            imageattach=imageattach,
            thoi_gian_release=datetimenow,
            id_user=id_user,
            user_name=thong_tin["user_name"],
            avatar_user=thong_tin["avatar_user"],
            so_thu_tu_su_kien=so_thu_tu_su_kien,
            location=thong_tin["location"],
        )

        # add
        db.session.add(new_comment)
        # commit
        db.session.commit()
        # lấy kết quả
        results1 = Comment.query.filter(
            Comment.id_toan_bo_su_kien == id_toan_bo_su_kien,
            Comment.so_thu_tu_su_kien == so_thu_tu_su_kien,
        ).count()
        if results1:
            saved_sukien.count_comment = results1
        db.session.commit()
        # lay notifi
        id_notifi = db.session.query(func.max(SavedNotifi.id)).scalar()
        id_notif = 0
        if id_notifi.id is not None:
            id_notif = id_notifi.id + 1
        else:
            id_notif = id_notif + 1
        # lay thong tin user
        profile_user = Users.query.filter(Users.id_user == id_user).first()
        if profile_user:
            user_name = profile_user.user_name
            link_avt = profile_user.link_avatar
        else:
            user_name = "Guest"
            link_avt = None
        status = "chua xem"
        # new notifi
        new_notifi = SavedNotifi(
            id=id_notif,
            id_user=id_user_comment,
            id_toan_bo_su_kien=id_toan_bo_su_kien,
            so_thu_tu_su_kien=so_thu_tu_su_kien,
            user_name=user_name,
            link_avatar=link_avt,
            link_imagesk=link_imagesk,
            status=status,
            thoigian=datetimenow,
        )
        db.session.add(new_notifi)
        db.session.commit()

        link = (
            f"https://photo.gachmen.org/detail/{id_toan_bo_su_kien}/{so_thu_tu_su_kien}"
        )
        message = f"User {user_name} comment on your post, click {link} to view detail!"

        await send_email_to_notifi(ketqua_user[0][6], message)  # send email by email

        return JSONResponse(content={"comment": thong_tin})
    except Exception as error:
        db.session.rollback()
        print(f"Failed------------: {error}")
        return {"error": f"Error Exception-----------: {error}"}


@app.get("/notification/{id_user}")
async def show_notifi(id_user: int):
    print("hello")
    thong_tin = {}
    list_thong_tin = []
    try:
        result2 = SavedNotifi.query.filter(
            SavedNotifi.id_user == id_user, SavedNotifi.status != "da vao link"
        ).all()
        result_toan_bo_su_kien = len(result2)
        print(result_toan_bo_su_kien)

        for i in result2:
            thong_tin["id_notifi"] = i.id
            thong_tin["id_user"] = i.id_user
            thong_tin["id_toan_bo_su_kien"] = i.id_toan_bo_su_kien
            thong_tin["so_thu_tu_su_kien"] = i.so_thu_tu_su_kien
            thong_tin["user_name"] = i.user_name
            thong_tin["link_avatar"] = i.link_avatar
            thong_tin["link_imagesk"] = i.link_imagesk
            thong_tin["status"] = i.status
            thong_tin["thoigian"] = i.thoigian
            thong_tin["num_notif"] = result_toan_bo_su_kien
            list_thong_tin.append(thong_tin)

        print("data succes", list_thong_tin)

        return {"notifi": list_thong_tin}
    except Exception as error:
        db.session.rollback()
        print(f"Error Exception: {error}")


@app.patch("/notification/update/{id_user}")
async def update_notifi(id_user: int):
    try:
        update_notifi = SavedNotifi.query.filter_by(id_user=id_user).filter()
        if update_notifi:
            for notification in update_notifi:
                notification.status = "da xem"

            db.session.commit()
            return {"message": "Notification updated successfully"}
        else:
            raise HTTPException(
                status_code=404, detail="No notifications found for this user."
            )
    except Exception as e:
        return {"error exeption------": str(e)}


@app.delete("/notification/delete/{id_user}/{id_notifi}")
async def delete_notifi(id_user: int, id_notifi: int):
    try:
        delete_notifi = SavedNotifi.query.filter(
            SavedNotifi.id_user == id_user, SavedNotifi.id == id_notifi
        ).first()
        db.session.delete(delete_notifi)
        db.session.commit()
        return {"message": "notification delete successfully"}
    except Exception as e:
        return {"error exeption": str(e)}


@app.post("/countview")
async def count_view(
    id_toan_bo_su_kien: str = Form(...), so_thu_tu_su_kien: str = Form(...)
):
    result = (
        db.session.query(SavedSuKien.count_view)
        .filter(
            SavedSuKien.id_toan_bo_su_kien == id_toan_bo_su_kien,
            SavedSuKien.so_thu_tu_su_kien == so_thu_tu_su_kien,
        )
        .first()
    )
    if result is not None:
        current_count_view = int(result[0])
        print(current_count_view)

        # Increment the count_view
        new_count_view = current_count_view + 1

        # Update
        db.session.query(SavedSuKien).filter(
            SavedSuKien.id_toan_bo_su_kien == id_toan_bo_su_kien,
            SavedSuKien.so_thu_tu_su_kien == so_thu_tu_su_kien,
        ).update({"count_view": new_count_view})

        # Commit
        db.session.commit()

        return {"count_view": new_count_view}
    return {"count_view": result}


@app.post("/saveimage/{id_user}", dependencies=[Depends(validate_token)])
async def save_image(id_user: int, request: Request):
    print("hello")
    results1 = []
    list_img = []
    image_urls = await request.json()
    list_image = []

    try:
        json_str = json.dumps(image_urls)
        json_obj = json.loads(json_str)
        for key in json_obj:
            max_id_user = db.session.query(func.max(SavedImage.id)).scalar()
            if max_id_user:
                id_img = max_id_user + 1
            else:
                id_img = 1
            dt_utc = datetime.now()
            tz = pytz.timezone("Asia/Bangkok")
            dt_local = dt_utc.astimezone(tz)
            date = dt_local.strftime("%Y-%m-%d, %H:%M:%S")
            # Thêm một dict mới vào list_image
            image_dict = {"id": id_img, "image_url": json_obj[key], "date": date}
            list_image.append(image_dict)

        for image in list_image:
            new_img = SavedImage(
                id=image["id"],
                id_user=id_user,
                link_image=image["image_url"],
                thoigian=image["date"],
            )
            db.session.add(new_img)
            db.session.commit()

        # lấy kết quả
        results1 = SavedImage.query.filter(SavedImage.id_user == id_user).all()

        for i in results1:
            list_img.append(i)

        return {"list_img": list_img}
    except Exception as error:
        db.session.rollback()
        print(f"Error Exeption: {error}")
        return JSONResponse(content={"Error Exeption"}, status_code=500)


@app.post("/changeavatar/{id_user}", dependencies=[Depends(validate_token)])
async def change_avatar(request: Request, id_user: int):
    form_data = await request.form()
    link_img = form_data.get("link_img")
    check_img = form_data.get("check_img")

    if not link_img:
        return "Link img can not None!"
    if not check_img:
        return "Check img can not None!"
    if link_img.startswith("/var/www"):
        link_img = link_img.replace(
            "/var/www/build_futurelove/", "https://photo.gachmen.org/"
        )
    db.session.query(Users).filter(Users.id_user == id_user).update(
        Users.link_avatar == link_img
    )
    db.session.commit()

    if check_img == "upload":
        max_id_user = db.session.query(func.max(SavedImage.id)).first()
        id_img = max_id_user + 1
        dt_utc = datetime.now()
        tz = pytz.timezone("Asia/Bangkok")
        dt_local = dt_utc.astimezone(tz)
        date = dt_local.strftime("%Y-%m-%d %H:%M:%S")
        new_avatar = SavedImage(
            id=id_img, id_user=id_user, link_image=link_img, thoigian=date
        )
        db.session.add(new_avatar)
        db.session.commit()

    return {"link_img": link_img}


@app.get("/search")
def search_word(request: Request):
    search_word = request.query_params.get("word")
    list_toan_bo_sukien_saved = []
    id_sukien = []
    stt_sukien = []
    thoi_gian_sk = []
    try:
        search_results = Comment.query.filter(
            func.upper(Comment.noi_dung_Comment).ilike(func.upper(f"%{search_word}%"))
        ).all()
        search_results2 = AddSuKien.query.filter(
            func.upper(Comment.noi_dung_Comment).ilike(func.upper(f"%{search_word}%"))
        ).all()

        for row in search_results:
            id_sukien.append(row.id_toan_bo_su_kien)
            stt_sukien.append(row.so_thu_tu_su_kien)
            thoi_gian_sk.append(row.thoi_gian_release)
        for row in search_results2:
            id_sukien.append(row.id_toan_bo_su_kien)
            stt_sukien.append(row.so_thu_tu_su_kien)
            thoi_gian_sk.append(row.thoigian_themsk)

        combined_list = list(set(zip(id_sukien, stt_sukien, thoi_gian_sk)))

        # Sắp xếp danh sách theo thời gian
        sorted_list = sorted(
            combined_list,
            key=lambda x: datetime.strptime(x[2], "%Y-%m-%d %H:%M:%S"),
            reverse=True,
        )

        latest_dict = {}

        for item in sorted_list:
            first_two = item[:2]
            if first_two not in latest_dict:
                latest_dict[first_two] = item
            else:
                current_time = item[2]
                existing_time = latest_dict[first_two][2]
                if current_time > existing_time:
                    latest_dict[first_two] = item

        filtered_list = list(latest_dict.values())

        for i in range(len(filtered_list)):
            Mot_LanQuerryData = []
            result2 = SavedSuKien.query.filter(
                SavedSuKien.id_toan_bo_su_kien == i
            ).all()
            thong_tin = {}
            for a in result2:
                thong_tin["id"] = a.id_saved
                thong_tin["link_nam_goc"] = a.link_nam_goc
                thong_tin["link_nu_goc"] = a.link_nu_goc
                thong_tin["link_nam_chua_swap"] = a.link_nam_chua_swap
                thong_tin["link_nu_chua_swap"] = a.link_nu_chua_swap
                thong_tin["link_da_swap"] = a.link_da_swap
                thong_tin["real_time"] = a.thoigian_swap
                thong_tin["ten_su_kien"] = a.ten_su_kien
                thong_tin["noi_dung_su_kien"] = a.noidung_su_kien
                thong_tin["id_toan_bo_su_kien"] = a.id_toan_bo_su_kien
                thong_tin["so_thu_tu_su_kien"] = a.so_thu_tu_su_kien
                thong_tin["id_user"] = a.id_user
                thong_tin["phantram_loading"] = a.phantram_loading
                thong_tin["count_comment"] = a.count_comment
                thong_tin["count_view"] = a.count_view
                thong_tin["ten_nam"] = a.ten_nam
                thong_tin["ten_nu"] = a.ten_nu
                thong_tin["id_template"] = a.id_template
                Mot_LanQuerryData.append(thong_tin)

                thong_tin = {}
            list_toan_bo_sukien_saved.append({"sukien": Mot_LanQuerryData})

        print("data succes", list_toan_bo_sukien_saved)

        return {"list_sukien": list_toan_bo_sukien_saved}
    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"


@app.get("/lovehistory/comment/{so_thu_tu_su_kien}")
async def get_comment_history(request: Request, so_thu_tu_su_kien: int, id_user: int):
    thong_tin = {}
    list_thong_tin = []
    id_toan_bo_su_kien = request.query_params.get("id_toan_bo_su_kien")
    id_user = request.query_params.get("id_user")

    try:
        result2 = Comment.query.filter(
            Comment.id_toan_bo_su_kien == id_toan_bo_su_kien,
            Comment.so_thu_tu_su_kien == so_thu_tu_su_kien,
        ).all()
        id_block_user = (
            db.session.query(BlockUser.id_block)
            .filter(BlockUser.id_user_report == id_user)
            .first()
        )
        # Lấy giá trị của phần tử thứ 7 trong mỗi item trong list2
        values_to_check = [item.id_block for item in id_block_user]
        # Tạo danh sách mới chỉ chứa các phần tử không trùng khớp
        result2 = [item for item in result2 if item.id_user not in values_to_check]
        # print(result_toan_bo_su_kien)
        for i in result2:
            thong_tin["id_toan_bo_su_kien"] = i.id_toan_bo_su_kien
            thong_tin["noi_dung_cmt"] = i.noi_dung_Comment
            thong_tin["dia_chi_ip"] = i.IP_Comment
            thong_tin["device_cmt"] = i.device_Comment
            thong_tin["id_comment"] = i.id_Comment
            thong_tin["imageattach"] = i.imageattach
            thong_tin["thoi_gian_release"] = i.thoi_gian_release
            thong_tin["user_name"] = i.user_name
            thong_tin["id_user"] = i.id_user
            thong_tin["avatar_user"] = i.avatar_user
            thong_tin["so_thu_tu_su_kien"] = so_thu_tu_su_kien
            thong_tin["location"] = i.location
            # save su kien
            saved_sukien = SavedSuKien.query.filter(
                SavedSuKien.id_toan_bo_su_kien == i.id_toan_bo_su_kien
            ).all()
            thong_tin["link_nam_goc"] = saved_sukien.link_nam_goc
            thong_tin["link_nu_goc"] = saved_sukien.link_nu_goc
            list_thong_tin.append(thong_tin)

        print("data success", list_thong_tin)

        return {"comment": list_thong_tin}
    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"


@app.get("/lovehistory/pageComment/{page}")
def get_page_comment_history(request: Request, page: int, id_user: int):
    thong_tin = {}
    id_user = request.query_params.get("id_user")
    if id_user:
        id_user = id_user
    else:
        id_user = 0
    Mot_LanQuerryData = []
    try:
        id_user_comment = (
            db.session.query(Comment.id_Comment, Comment.id_user)
            .order_by(Comment.thoi_gian_release.desc())
            .all()
        )
        id_block_user = (
            db.session.query(BlockUser.id_block)
            .filter(BlockUser.id_user_report == id_user)
            .all()
        )

        # Tạo danh sách các id_block từ kết quả
        values_to_check = [item[0] for item in id_block_user] if id_block_user else []

        # Tạo danh sách mới chỉ chứa các phần tử không trùng khớp
        result = [item for item in id_user_comment if item[1] not in values_to_check]

        records = []
        for row in result:
            id_toan_bo_su_kien = row[0]
            records.append(id_toan_bo_su_kien)
        soPhanTuTrenMotTrang = 10
        soTrang = (len(records) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang
        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(records))
        else:
            return {"message": "exceed the number of pages"}
        print("hello")
        for i in range(start, end):
            idItemPhanTu = records[i]
            result2 = Comment.query.filter(Comment.id_Comment == idItemPhanTu).all()
            thong_tin = {}
            for i in result2:
                thong_tin["id_toan_bo_su_kien"] = i.id_toan_bo_su_kien
                thong_tin["so_thu_tu_su_kien"] = (
                    0 if i.so_thu_tu_su_kien is None else i.so_thu_tu_su_kien
                )
                thong_tin["noi_dung_cmt"] = i.noi_dung_Comment
                thong_tin["dia_chi_ip"] = i.IP_Comment
                thong_tin["device_cmt"] = i.device_Comment
                thong_tin["id_comment"] = i.id_Comment
                thong_tin["imageattach"] = i.imageattach
                thong_tin["thoi_gian_release"] = i.thoi_gian_release
                thong_tin["user_name"] = i.user_name
                thong_tin["id_user"] = i.id_user
                thong_tin["avatar_user"] = i.avatar_user
                thong_tin["location"] = i.location
                thong_tin["link_nam_goc"] = "0"
                thong_tin["link_nu_goc"] = "0"
                # saved su kien
                saved_sukien = SavedSuKien.query.filter(
                    SavedSuKien.id_toan_bo_su_kien == i.id_toan_bo_su_kien
                ).all()

                if saved_sukien:
                    thong_tin["link_nam_goc"] = saved_sukien.link_nam_goc
                    thong_tin["link_nu_goc"] = saved_sukien.link_nu_goc

            Mot_LanQuerryData.append(thong_tin)

        return JSONResponse(content={"comment": Mot_LanQuerryData})
    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"


# tim theo id user
@app.get("/lovehistory/user/{id_user}")
async def get_data_love_history_user(request: Request, id_user: int):
    info = {}
    list_event = []

    try:
        result = (
            db.session.query(
                SavedSuKien.id_toan_bo_su_kien, func.max(SavedSuKien.thoigian_swap)
            )
            .filter(SavedSuKien.id_user == id_user)
            .group_by(SavedSuKien.id_toan_bo_su_kien)
            .order_by(func.max(SavedSuKien.thoigian_swap).desc())
            .all()
        )

        for index in result2:
            idItem = index.id_saved
            data = []

            result2 = SavedSuKien.query.filter(
                SavedSuKien.id_toan_bo_su_kien == idItem
            ).all()
            for i in result2:
                info = {}
                info["id"] = i.id_saved
                info["link_nam_goc"] = i.link_nam_goc
                info["link_nu_goc"] = i.link_nu_goc
                info["link_nam_chua_swap"] = i.link_nam_chua_swap
                info["link_nu_chua_swap"] = i.link_nu_chua_swap
                info["link_da_swap"] = i.link_da_swap
                info["real_time"] = i.thoigian_swap
                info["ten_su_kien"] = i.ten_su_kien
                info["noi_dung_su_kien"] = i.noidung_su_kien
                info["id_toan_bo_su_kien"] = i.id_toan_bo_su_kien
                info["so_thu_tu_su_kien"] = i.so_thu_tu_su_kien
                info["id_user"] = i.id_user
                info["phantram_loading"] = i.phantram_loading
                info["count_comment"] = i.count_comment
                info["count_view"] = i.count_view
                info["ten_nam"] = i.ten_nam
                info["ten_nu"] = i.ten_nu
                info["id_template"] = i.id_template
                data.append(info)

            list_event.append({"sukien": data})

        return JSONResponse(content={"list_sukien": list_event})
    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"


@app.get("/lovehistory/comment/user/{id_user}")
def get_Comment_History_User(id_user: int):
    thong_tin = {}
    list_thong_tin = []

    try:
        result2 = Comment.query.filter(Comment.id_user == id_user).all()
        toan_bo_comment = len(result2)
        print("toan bo comment", toan_bo_comment)

        for i in result2:
            thong_tin["id_toan_bo_su_kien"] = i.id_toan_bo_su_kien
            thong_tin["noi_dung_cmt"] = i.noi_dung_Comment
            thong_tin["dia_chi_ip"] = i.IP_Comment
            thong_tin["device_cmt"] = i.device_Comment
            thong_tin["id_comment"] = i.id_Comment
            thong_tin["imageattach"] = i.imageattach
            thong_tin["thoi_gian_release"] = i.thoi_gian_release
            thong_tin["user_name"] = i.user_name
            thong_tin["id_user"] = i.id_user
            thong_tin["avatar_user"] = i.avatar_user
            thong_tin["so_thu_tu_su_kien"] = i.so_thu_tu_su_kien
            thong_tin["location"] = i.location
            thong_tin["link_nam_goc"] = "0"
            thong_tin["link_nu_goc"] = "0"

            saved_sukien = SavedSuKien.query.filter(
                SavedSuKien.id_toan_bo_su_kien == i.id_toan_bo_su_kien
            ).all()

            if saved_sukien:
                thong_tin["link_nam_goc"] = saved_sukien.link_nam_goc
                thong_tin["link_nu_goc"] = saved_sukien.link_nu_goc
                result3 = Users.query.filter(
                    Users.id_user == saved_sukien.id_user
                ).first()
                thong_tin["user_taosk"] = result3.id_user

            list_thong_tin.append(thong_tin)

        print("data success", list_thong_tin)
        return JSONResponse(content={"comment_user": list_thong_tin})

    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"


@app.get("/lovehistory/page/{page}")
async def get_page_love_history(request: Request, page: int, id_user: int):
    list_toan_bo_sukien_saved = []
    id_user = request.query_params.get("id_user")
    if id_user:
        id_user = id_user
    else:
        id_user = 0

    try:
        result = (
            db.session.query(
                SavedSuKien.id_toan_bo_su_kien,
                func.max(SavedSuKien.thoigian_swap),
                SavedSuKien.id_user,
            )
            .group_by(SavedSuKien.id_user, SavedSuKien.id_toan_bo_su_kien)
            .order_by(func.max(SavedSuKien.thoigian_swap))
            .all()
        )
        id_block_user = (
            db.session.query(BlockUser.id_block)
            .filter(BlockUser.id_user_report == id_user)
            .all()
        )
        print("------id block user-------", id_block_user)
        values_to_check = [item[0] for item in id_block_user]
        # Tạo danh sách mới chỉ chứa các phần tử không trùng khớp
        result = [item for item in result if item[2] not in values_to_check]

        records = []
        for row in result:
            id_toan_bo_su_kien = row[0]
            records.append(id_toan_bo_su_kien)

        soPhanTuTrenMotTrang = 8
        soTrang = (len(records) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang

        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(records))
        else:
            return JSONResponse(content="exceed the number of pages!!!")
        print("hello")
        for i in range(start, end):
            idItemPhanTu = records[i]
            Mot_LanQuerryData = []

            result2 = SavedSuKien.query.filter(
                SavedSuKien.id_toan_bo_su_kien == idItemPhanTu
            ).all()
            thong_tin = {}
            for i in result2:
                thong_tin["id"] = i.id_saved
                if i.link_nam_goc.find("https://futurelove.online") > 0:
                    thong_tin["link_nam_goc"] = i.link_nam_goc.replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_nam_goc"] = i.link_nam_goc
                if i.link_nu_goc.find("https://futurelove.online") > 0:
                    thong_tin["link_nu_goc"] = i.link_nu_goc.replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_nu_goc"] = i.link_nu_goc
                if i.link_nam_chua_swap.find("https://futurelove.online") > 0:
                    thong_tin["link_nam_chua_swap"] = i.link_nam_chua_swap.replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_nam_chua_swap"] = i.link_nam_chua_swap
                if i.link_nu_chua_swap.find("https://futurelove.online") > 0:
                    thong_tin["link_nu_chua_swap"] = i.link_nu_chua_swap.replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_nu_chua_swap"] = i.link_nu_chua_swap
                if i.link_da_swap.find("https://futurelove.online") > 0:
                    thong_tin["link_da_swap"] = i.link_da_swap.replace(
                        "https://futurelove.online", "https://photo.gachmen.org"
                    )
                else:
                    thong_tin["link_da_swap"] = i.link_da_swap
                thong_tin["real_time"] = i.thoigian_swap
                thong_tin["ten_su_kien"] = i.ten_su_kien
                thong_tin["noi_dung_su_kien"] = i.noidung_su_kien
                thong_tin["id_toan_bo_su_kien"] = i.id_toan_bo_su_kien
                thong_tin["so_thu_tu_su_kien"] = i.so_thu_tu_su_kien
                thong_tin["id_user"] = i.id_user
                thong_tin["phantram_loading"] = i.phantram_loading
                thong_tin["count_comment"] = i.count_comment
                thong_tin["count_view"] = i.count_view
                thong_tin["ten_nam"] = i.ten_nam
                thong_tin["ten_nu"] = i.ten_nu
                thong_tin["id_template"] = i.id_template
                Mot_LanQuerryData.append(thong_tin)

            list_toan_bo_sukien_saved.append({"sukien": Mot_LanQuerryData})

        return JSONResponse(content={"list_sukien": list_toan_bo_sukien_saved})
    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"


@app.post(
    "/lovehistory/add/{id_toan_bo_su_kien}", dependencies=[Depends(validate_token)]
)
async def add_Them_Su_Kien_Tinh_Yeu(
    id_toan_bo_su_kien: int,
    request: Request,
    ten_sukien: str = Form(...),
    noidung_su_kien: str = Form(...),
    ten_nam: str = Form(...),
    ten_nu: str = Form(...),
    device_them_su_kien: str = Form(...),
    ip_them_su_kien: str = Form(...),
    link_img: str = Form(...),
    link_video: str = Form(...),
    id_user: int = Form(...),
    id_template: int = Form(...),
):
    link1 = request.headers.get("Link1")
    link2 = request.headers.get("Link2")
    try:
        max_sql_id_saved = db.session.query(func.max(AddSuKien.id_add)).scalar()
        print("idmas", max_sql_id_saved)
        if max_sql_id_saved is not None:
            id_add_max = max_sql_id_saved + 1
        else:
            id_add_max = 1
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        max_stt_skien = (
            db.session.query(func.max(SavedSuKien.so_thu_tu_su_kien))
            .filter(SavedSuKien.id_toan_bo_su_kien == id_toan_bo_su_kien)
            .first()
        )
        so_thu_tu_sk = (max_stt_skien[0] or 0) + 1

        count_comment = 0
        count_view = 0
        status = "Ok!"
        add_sukien = AddSuKien(
            id_add=id_add_max,
            id_user=id_user,
            id_toan_bo_su_kien=id_toan_bo_su_kien,
            ten_sukien=ten_sukien,
            noidung_su_kien=noidung_su_kien,
            ten_nam=ten_nam,
            ten_nu=ten_nu,
            device_them_su_kien=device_them_su_kien,
            ip_them_su_kien=ip_them_su_kien,
            link_img=link_img,
            link_video=link_video,
            id_template=id_template,
            thoigian_themsk=date,
            so_thu_tu_su_kien=so_thu_tu_sk,
            count_comment=count_comment,
            count_view=count_view,
            status=status,
        )
        db.session.add(add_sukien)
        db.session.commit()
        link_nam_chua_swap = "abc"
        link_nu_chua_swap = "abc"

        if link_img is None:
            link_swap = link_video
        else:
            link_swap = link_img

        print(link_swap)
        phantram_loading = 0
        add_saved_sukien = SavedSuKien(
            id_saved=id_toan_bo_su_kien,
            link_nam_goc=link1,
            link_nu_goc=link2,
            link_nam_chua_swap=link_nam_chua_swap,
            link_nu_chua_swap=link_nu_chua_swap,
            link_da_swap=link_swap,
            thoigian_swap=date,
            ten_su_kien=ten_sukien,
            noidung_su_kien=noidung_su_kien,
            id_toan_bo_su_kien=id_toan_bo_su_kien,
            so_thu_tu_su_kien=so_thu_tu_sk,
            thoigian_sukien=date,
            device_them_su_kien=device_them_su_kien,
            ip_them_su_kien=ip_them_su_kien,
            id_user=id_user,
            tomLuocText=noidung_su_kien,
            ten_nam=ten_nam,
            ten_nu=ten_nu,
            count_comment=count_comment,
            count_view=count_view,
            id_template=id_template,
            phantram_loading=phantram_loading,
        )
        db.session.add(add_saved_sukien)
        db.session.commit()

        print("data success", add_saved_sukien)
        return {"message": "successfully added event", "data": add_saved_sukien}
    except Exception as error:
        db.session.rollback()
        print(f"Error exception: {error}")
        return {"ketqua": "Error exception: " + str(error)}


@app.get("/profile/{id_user}")
async def info_user(id_user: str):
    user = Users.query.filter(Users.id_user == id_user).all()

    count_comment = Comment.query.filter(Comment.id_user == id_user).count()
    count_sk = (
        db.session.query(func.count(func.distinct(SavedSuKien.id_toan_bo_su_kien)))
        .filter(SavedSuKien.id_user == id_user)
        .scalar()
    )

    if user:
        user.count_comment = count_comment
        user.count_sukien = count_sk
        db.session.commit()
    thong_tin = {}
    for i in user:
        thong_tin["id_user"] = i
        thong_tin["link_avatar"] = i.link_avatar
        thong_tin["user_name"] = i.user_name
        thong_tin["ip_register"] = i.ip_register
        thong_tin["device_register"] = i.device_register
        thong_tin["email"] = i.email
        thong_tin["count_sukien"] = i.count_sukien
        thong_tin["count_comment"] = i.count_comment
        thong_tin["count_view"] = i.count_view

    return JSONResponse(content=thong_tin)


@app.get("/profile/user/{name}")
async def info(name: str):
    user = Users.query.filter_by(Users.user_name.ilike(f"%{name}%")).all()
    for item in user:
        count_comment = Comment.query.filter(Comment.id_user == item.id_user).count()
        count_sk = count_sk = (
            db.session.query(func.count(SavedSuKien.id_toan_bo_su_kien.distinct()))
            .filter(SavedSuKien.id_user == item.id_user)
            .scalar()
        )
        if user:
            user.count_comment = count_comment
            user.count_sukien = count_sk
            db.session.commit()

    list_thongtin = []
    for i in user:
        thong_tin = {}
        thong_tin["id_user"] = i.id_user
        thong_tin["link_avatar"] = i.link_avatar
        thong_tin["user_name"] = i.user_name
        thong_tin["ip_register"] = i.ip_register
        thong_tin["device_register"] = i.device_register
        thong_tin["email"] = i.email
        thong_tin["count_sukien"] = i.count_sukien
        thong_tin["count_comment"] = i.count_comment
        thong_tin["count_view"] = i.count_view
        list_thongtin.append(thong_tin)
    return JSONResponse(content=list_thongtin)


@app.post("/register/user")
async def register_user(request: Request):
    form_data = await request.form()
    user_name = form_data.get("user_name")
    password = form_data.get("password")
    email = form_data.get("email")
    ip_register = form_data.get("ip_register")
    device_register = form_data.get("device_register")
    link_avatar = form_data.get("link_avatar")
    if link_avatar.startswith("/var/www/"):
        link_avatar = link_avatar.replace(
            "/var/www/build_futurelove/", "https://photo.gachmen.org/"
        )
    # print("______USERNAME: " + user_name, password)
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    match = re.match(pattern, password)
    if not user_name or not password or not email:
        return JSONResponse(content={"message": "Fields cannot be left blank."})

    if len(password) < 6:
        return JSONResponse(
            content={"message": "Password must have at least 6 characters."}
        )

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.[\w-]+$", email):
        return JSONResponse(content={"message": "Email invalidate"})

    account = Users.query.filter(Users.email == email).filter()
    if account:
        return JSONResponse(content={"message": "Account already exists!"})
    else:
        data = {
            "email": email,
            "password": password,
            "username": user_name,
            "linkavt": link_avatar,
            "ip": ip_register,
            "device": device_register,
        }
        token = jwt.encode(data, secret_key, algorithm="HS256")
        await save_user_to_mysql(
            user_name,
            password,
            email,
            link_avatar,
            ip_register,
            device_register,
            "email",
        )
        link = request.url_for("register_confirm", token=token)
        await send_mail_to_email(email, link, user_name, password)
        return JSONResponse(
            content={
                "message": "Successfully registered",
                "account": {"email": email},
            }
        )


@router.get("/register_confirm/{token}")
async def register_confirm(token: str):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        emailCheck = decoded_token["email"]
        user = Users.query.filter(Users.email == emailCheck).filter()
        # print("_____" + str(mycursor))
        # print("___SONPRO___" + str(ketqua))
        # print(str(num_rows))
        if user:
            return JSONResponse(
                content={
                    "message": "email register exist, please register another email"
                }
            )
        await save_user_to_mysql(
            decoded_token["username"],
            decoded_token["password"],
            decoded_token["email"],
            decoded_token["linkavt"],
            decoded_token["ip"],
            decoded_token["device"],
            "email",
        )

        return JSONResponse(content={"message": "Confirm successful registration"})

    except jwt.exceptions.DecodeError:
        db.session.rollback()
        return JSONResponse(content={"message": "Invalid token"})


app.include_router(router)


@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    user_name = form_data.get("email_or_username")
    password = form_data.get("password")
    print("______________user_name______", str(user_name))
    print("______________password______", str(password))

    if not user_name or not password:
        return JSONResponse(
            content={
                "message": "Fields email_or_username and password cannot be left blank."
            }
        )
    thong_tin = {}
    try:
        user = Users.query.filter(
            or_(Users.user_name == user_name, Users.email == user_name)
        ).first()
        print("user_name___" + str(user_name) + "____email___" + str(password))
        if len(user) == 0:
            thong_tin["id_user"] = ""
            thong_tin["link_avatar"] = ""
            thong_tin["user_name"] = ""
            thong_tin["ip_register"] = ""
            thong_tin["device_register"] = ""
            thong_tin["email"] = ""
            thong_tin["count_sukien"] = ""
            thong_tin["count_comment"] = ""
            thong_tin["count_view"] = ""
            thong_tin["message"] = "Account Not Found - Please Recheck Account " + str(
                user_name
            )
            thong_tin["status"] = 300
            return thong_tin
        if user:
            if user[0][5] == password:
                thong_tin["id_user"] = user[0][0]
                thong_tin["link_avatar"] = user[0][1]
                thong_tin["user_name"] = user[0][2]
                thong_tin["ip_register"] = user[0][3]
                thong_tin["device_register"] = user[0][4]
                thong_tin["email"] = user[0][6]
                thong_tin["count_sukien"] = int(user[0][7])
                thong_tin["count_comment"] = int(user[0][8])
                thong_tin["count_view"] = int(user[0][9])
                thong_tin["time_coin"] = int(user[0][13])
                thong_tin["message"] = "Success Login Account"
                if isinstance(thong_tin, dict):
                    token = generate_token(user_name)
                    thong_tin["token"] = token
                    thong_tin["status"] = 200
                    return thong_tin
            else:
                thong_tin["id_user"] = ""
                thong_tin["link_avatar"] = ""
                thong_tin["user_name"] = ""
                thong_tin["ip_register"] = ""
                thong_tin["device_register"] = ""
                thong_tin["email"] = ""
                thong_tin["count_sukien"] = ""
                thong_tin["count_comment"] = ""
                thong_tin["count_view"] = ""
                thong_tin["message"] = "Wrong Password! "
                thong_tin["status"] = 301
                return thong_tin
        else:
            thong_tin["id_user"] = ""
            thong_tin["link_avatar"] = ""
            thong_tin["user_name"] = ""
            thong_tin["ip_register"] = ""
            thong_tin["device_register"] = ""
            thong_tin["email"] = ""
            thong_tin["count_sukien"] = ""
            thong_tin["count_comment"] = ""
            thong_tin["count_view"] = ""
            thong_tin["message"] = "Account Not Found - Please Recheck Account " + str(
                user_name
            )
            thong_tin["status"] = 302
            return thong_tin

    except Exception as error:
        db.session.rollback()
        print(f"Error Exception: {error}")
    thong_tin["id_user"] = ""
    thong_tin["link_avatar"] = ""
    thong_tin["user_name"] = ""
    thong_tin["ip_register"] = ""
    thong_tin["device_register"] = ""
    thong_tin["email"] = ""
    thong_tin["count_sukien"] = ""
    thong_tin["count_comment"] = ""
    thong_tin["count_view"] = ""
    thong_tin["message"] = "Account Not Found - Please Recheck Account " + str(
        user_name
    )
    thong_tin["status"] = 304
    return thong_tin


@app.post("/reset")
async def reset_password(request: Request):
    try:
        form_data = await request.form()
        email = form_data.get("email")
        print(email)
        email_user = db.session.query(Users.email).filter(Users.email == email).first()
        print(email_user)
        if email_user:
            # Generate a new password
            new_uuid = uuid.uuid4()
            uuid_str = str(new_uuid).replace("-", "")[:12]
            new_password = uuid_str
            # Send email with the new password
            await send_mail_to_email_reset(email, new_password)  # send email by email
            if email_user:
                email_user.password = new_password
                db.session.commit()
            return {"message": "Password reset successfully and email sent!"}
        else:
            # Raise exception if no user with the provided email is found
            raise HTTPException(
                status_code=404, detail=f"No user with email found: {email}"
            )
    except Exception as e:
        db.session.rollback()
        return JSONResponse(content={"message": f"Error: {e}", "status": 500})


@app.post("/changepassword/{id_user}", dependencies=[Depends(validate_token)])
async def change_password(request: Request, id_user: str):
    form_data = await request.form()
    old_password = form_data.get("old_password")
    new_password = form_data.get("new_password")
    user = Users.query.filter(
        Users.id_user == id_user, Users.password == old_password
    ).filter()
    thong_tin = {}
    if user is None:
        raise HTTPException(status_code=400, detail="Password Incorrect!.")

    for row in user:
        if user:
            user.password = new_password
            db.session.commit

        thong_tin = {
            "id_user": row.id_user,
            "link_avatar": row.link_avatar,
            "user_name": row.user_name,
            "ip_register": row.ip_register,
            "device_register": row.device_register,
            "email": row.email,
            "count_sukien": row.count_sukien,
            "count_comment": row.count_comment,
            "count_view": row.count_view,
        }

    return JSONResponse(content=thong_tin)


@app.post("/deleteuser/{id_user}", dependencies=[Depends(validate_token)])
async def del_user(id_user: int, request: Request):
    form_data = await request.form()
    password = form_data.get("password")
    email = form_data.get("email")
    try:
        passw = (
            db.session.query(Users.password, Users.email)
            .filter(Users.email == email, Users.password == password)
            .first()
        )
        print("-----email and password-----", passw)
        if passw is None:
            return JSONResponse(content="This user is not available!")
        user = Users.query.filter(Users.id_user == id_user).first()
        save_image = SavedImage.query.filter(SavedImage.id_user == id_user).all()
        comment = Comment.query.filter(Comment.id_user == id_user).all()
        saved_sukien = SavedSuKien.query.filter(SavedSuKien.id_user == id_user).all()
        saved_sukien_video = SavedSuKienVideo.query.filter(
            SavedSuKienVideo.id_user == id_user
        ).all()
        add_sukien = AddSuKien.query.filter(AddSuKien.id_user == id_user).all()
        saved_notification = SavedNotifi.query.filter(
            SavedNotifi.id_user == id_user
        ).all()

        # Create a list of all objects to delete
        obj_delete = (
            [user]
            + save_image
            + comment
            + saved_sukien
            + saved_sukien_video
            + add_sukien
            + saved_notification
        )
        for obj in obj_delete:
            if obj:
                db.session.delete(obj)
            else:
                print(
                    f"Delete user failed! password {passw} and email {email} are incorrect! Please check again !"
                )
        # commit
        db.session.commit()

        message = "Thank you for using our Future Love service, we look forward to your return one day soon!"
        await send_email_to_del_account(passw.password, message)  # send email to email

        # return JSONResponse(content="User and related records deleted successfully.")
        return JSONResponse(
            content={
                "message": "Successfully deleted account with id = {}".format(id_user)
            }
        )
    except Exception as error:
        db.session.rollback()
        print(f" Error Exception: {error}")
        return {f"Error Exception: {error}"}


@app.patch("/lovehistory/edit/{id_comment}", dependencies=[Depends(validate_token)])
async def update_comment(request: Request, id_comment: int):
    new_content = await request.json()
    try:
        update_comment = Comment.query.filter(Comment.id_Comment == id_comment).first()
        if update_comment:
            update_comment.noi_dung_comment = new_content["content"]
            db.session.commit()
            print("Comment updated successfully.")
        else:
            return {"Update comment failed"}
        return {"message": "Comment updated successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}


@app.delete("/lovehistory/delete/{id_comment}", dependencies=[Depends(validate_token)])
def delete_comment(id_comment: int):
    try:
        delete_query = Comment.query.filter(Comment.id_Comment == id_comment).first()
        if delete_query is None:
            return {"message": "Comment not found"}
        db.session.delete(delete_query)
        db.session.commit()
        return {"message": "Comment deleted successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}


@app.post("/report/sukien/{id_toan_bo_su_kien}/{so_thu_tu_su_kien}")
async def report_event(
    request: Request, id_toan_bo_su_kien: int, so_thu_tu_su_kien: int
):
    form_data = await request.form()
    report_reason = form_data.get("report_reason")
    id_user_report = form_data.get("id_user_report")
    id_user_sukien = form_data.get("id_user_sukien")

    try:
        add_sukien = AddSuKien.query.filter(
            AddSuKien.id_toan_bo_su_kien, AddSuKien.so_thu_tu_su_kien
        ).all()
        if add_sukien:
            add_sukien.status = "Report!"
            db.session.commit()
        new_report = ReportSuKien(
            id_toan_bo_su_kien=id_toan_bo_su_kien,
            so_thu_tu_su_kien=so_thu_tu_su_kien,
            report_reason=report_reason,
            id_user_report=id_user_report,
            id_user_sukien=id_user_sukien,
        )
        db.session.add(new_report)
        db.session.commit()
        print("data succes")
        return {"message": "Successfully event reported!"}
    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"


@app.post("/buy_coin_inapp")
async def buy_coin_inapp(request: Request):
    try:
        form_data = await request.form()
        coin_number = form_data.get("coin_number")
        user_id = form_data.get("user_id")
        if user_id == None:
            return {"message": "Body must have: user_id", "coin": 0, "user_id": 0}
        if coin_number == None:
            return {"message": "Body must have: coin_number", "coin": 0, "user_id": 0}
        user = Users.query.filter(Users.id_user == user_id).filter()
        if user:
            user.time_coin_in_app = coin_number
            db.session.commit()
        print("buy coin done")
    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"
    return {"message": "Done okie", "coin": coin_number, "user_id": user_id}


@app.get("/get_coin_inapp/{user_id}")
async def get_coin_inapp(user_id: str):
    try:
        coin_data = Users.query.filter(Users.id_user == user_id).filter()

        if coin_data == None:
            return {
                "message": "Successfully done data",
                "coin_number": 0,
                "user_id": user_id,
            }
        return {
            "message": "Successfully done data",
            "coin_number": coin_data.time_coin_in_app,
            "user_id": user_id,
        }
    except Exception as error:
        db.session.rollback()
        return {
            "message": "False Database Connect ____ {error}",
            "coin_number": 0,
            "user_id": user_id,
        }


@app.post("/report/comment")
async def report_comment(request: Request):
    form_data = await request.form()
    id_comment = form_data.get("id_comment")
    report_reason = form_data.get("report_reason")
    id_user_report = form_data.get("id_user_report")
    id_user_comment = form_data.get("id_user_comment")
    try:
        comment = Comment.query.filter(Comment.id_Comment == id_comment).first()
        id_rp = db.session.query(func.max(ReportComment.id_report)).scalar()
        if id_rp[0]:
            id_report = id_rp[0]
        else:
            id_report = 1
        if comment is not None:
            return {"message": "Comment not found"}
        # Get the next report ID
        id_rp = db.session.query(func.max(ReportComment.id_report)).scalar()
        id_report = (id_rp + 1) if id_rp is not None else 1
        add_report = Comment(
            id_report=id_report,
            id_comment=id_comment,
            report_reason=report_reason,
            content=comment.noi_dung_Comment,
            id_user_report=id_user_report,
            id_user_comment=id_user_comment,
        )
        db.session.add(add_report)
        db.session.commit()
        return {"message": "Successfully comment reported!"}
    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"


@app.post("/add/token")
async def add_token_ios(request: Request):
    form_data = await request.form()
    id_user = form_data.get("id_user")
    device_name = form_data.get("device_name")
    device_token = form_data.get("device_token")
    try:

        check_token = DeviceTokenIos.query.filter(
            DeviceTokenIos.device_token == device_token
        ).first()
        if check_token:
            return {"message": "Tokens are available!!"}

        new_token = DeviceTokenIos(
            id_user=id_user, device_name=device_name, device_token=device_token
        )
        db.session.add(new_token)
        db.session.commit()

        return {"message": "Successfully insert device_token!"}

    except Exception as error:
        db.session.rollback()
        return f"Error Exception: {error}"


def is_duplicate_image(src_img_path, folder_path):
    try:
        # print(src_img_path)
        with open(src_img_path, "rb") as f:
            src_img_data = f.read()
            src_img_base64 = base64.b64encode(src_img_data).decode("utf-8")
        # print("error here 1")
        for filename in os.listdir(folder_path):
            # print(f"filefilename)
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_base64 = base64.b64encode(file_data).decode("utf-8")
            if src_img_base64 == file_base64:
                return filename  # Trả về tên của tệp ảnh trùng lặp
        # print("error here 2")
        return None  # Trả về None nếu không có tệp ảnh trùng lặp
    except Exception as e:
        print(e)
        return JSONResponse(content=({"message": f"Error: {e}"}))


def copy_image(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)
        print("Tệp ảnh đã được sao chép thành công.")
    except FileNotFoundError:
        print(f"Tệp ảnh nguồn '{source_path}' không tồn tại.")
    except shutil.SameFileError:
        print(f"Tệp ảnh đích '{destination_path}' đã tồn tại.")


# ham zip file anh va video
def zip_images(base_dir, zip_name):
    # Đảm bảo rằng zip_name không chứa đường dẫn
    zip_name = os.path.basename(zip_name)

    # Tạo đường dẫn đầy đủ cho tệp zip trong thư mục codetime
    zip_path = os.path.join(base_dir, "..", zip_name)
    zip_path = os.path.abspath(zip_path)  # Đảm bảo đường dẫn tuyệt đối

    # Mở tệp zip để ghi
    with zipfile.ZipFile(zip_path, "w") as zipf:
        # Đi qua tất cả các tệp trong thư mục base_dir
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                # Kiểm tra xem tệp có phải là hình ảnh không (có phần mở rộng là .jpg hoặc .png)
                if file.endswith(".jpg") or file.endswith(".png"):
                    # Xác định đường dẫn đầy đủ của tệp
                    file_path = os.path.join(root, file)
                    # Tạo đường dẫn tương đối để thêm vào tệp zip
                    relative_path = os.path.relpath(file_path, base_dir)
                    # Thêm tệp vào tệp zip
                    zipf.write(file_path, relative_path)
    return zip_path


executor = ThreadPoolExecutor(max_workers=2)


@app.get("/getdata/Download", dependencies=[Depends(validate_token)])
async def run_task_in_background_growup_wedding(
    device_them_su_kien: str, ip_them_su_kien: str, id_user: str, folderLuu: str
):
    generated_uuid = uuid.uuid4().int
    id_download = str(generated_uuid)[-12:]
    link = f"https://makewedding.online/timeline/image/{id_download}"
    loop = asyncio.get_event_loop()

    zip_name = "video_image_" + str(id_user) + ".zip"
    data_zip = zip_images(folderLuu, zip_name)

    # return JSONResponse(content={"sukien_image": data})
    return data_zip


@app.post("/upload-gensk2/{id_user}")
async def update_comment(request: Request, id_user: int):
    new_json = await request.json()
    print(str(new_json))
    try:
        print(str(new_json))
        return JSONResponse(
            content=({"message": f"Error: {str(new_json)}", "status": 500})
        )
    except Exception as e:
        return {"error": str(e)}


@app.post("/upload-gensk/{id_user}")
async def upload_image(request: Request, id_user: int, src_img: UploadFile = File(...)):
    try:
        type = request.query_params.get("type")
        # Tạo folder để lưu ảnh (nếu chưa tồn tại)
        folder_path_temp = f"/var/www/build_futurelove/image/image_user/{id_user}/temp"
        folder_path_nam = f"/var/www/build_futurelove/image/image_user/{id_user}/nam"
        folder_path_video = (
            f"/var/www/build_futurelove/image/image_user/{id_user}/video"
        )
        folder_path_nu = f"/var/www/build_futurelove/image/image_user/{id_user}/nu"
        if not os.path.exists(folder_path_nam):
            os.makedirs(folder_path_nam)
        if not os.path.exists(folder_path_nu):
            os.makedirs(folder_path_nu)
        if not os.path.exists(folder_path_temp):
            os.makedirs(folder_path_temp)
        if not os.path.exists(folder_path_video):
            os.makedirs(folder_path_video)
        print("pass1")
        if type == "src_vid":
            file_name_video = f"{id_user}_vid_{random.randint(10000, 99999)}.jpg"
            src_video_path_temp = os.path.join(folder_path_temp, file_name_video)
            # print(src_video_path_temp)
            print("__________________IM IN__________________")
            with open(src_video_path_temp, "wb") as image:
                print("WRITE_IMAGE")
                image.write(src_img.file.read())

            source_face = get_one_face(cv2.imread(src_video_path_temp))
            print("I PASS THIS")
            if source_face is None:
                os.remove(src_video_path_temp)
                return {
                    "message": "We cannot identify the face in the photo you provided, please upload another photo"
                }

            is_duplicate = is_duplicate_image(src_video_path_temp, folder_path_video)
            print(is_duplicate)
            if is_duplicate:
                os.remove(src_video_path_temp)
                print("Vao 1")
                return f"{folder_path_video}/{is_duplicate}"
            else:
                src_vid_path = os.path.join(folder_path_video, file_name_video)
                copy_image(src_video_path_temp, src_vid_path)
                os.remove(src_video_path_temp)
                print("Vao 2")
                return f"{src_vid_path}"

        print("pass2")
        if type == "src_nam":
            # print("in")
            file_name_nam = f"{id_user}_nam_{random.randint(10000, 99999)}.jpg"
            src_nam_path_temp = os.path.join(folder_path_temp, file_name_nam)
            # print("pass 1")
            with open(src_nam_path_temp, "wb") as image:
                image.write(src_img.file.read())
            # print("pass 2")

            source_face = get_one_face(cv2.imread(src_nam_path_temp))
            if source_face is None:
                os.remove(src_nam_path_temp)
                return {
                    "message": "We cannot identify the face in the photo you provided, please upload another photo"
                }
            # print("pass 3")

            is_duplicate = is_duplicate_image(src_nam_path_temp, folder_path_nam)
            print(is_duplicate)
            if is_duplicate:
                os.remove(src_nam_path_temp)
                print("KHONG NONE")
                print(f"{folder_path_nam}/{is_duplicate}")
                return f"{folder_path_nam}/{is_duplicate}"
            else:
                src_nam_path = os.path.join(folder_path_nam, file_name_nam)
                copy_image(src_nam_path_temp, src_nam_path)
                os.remove(src_nam_path_temp)
                print(f"{src_nam_path}")
                print("Co NONE")
                return f"{src_nam_path}"

        if type == "src_nu":
            file_name_nu = f"{id_user}_nu_{random.randint(10000, 99999)}.jpg"
            src_nu_path_temp = os.path.join(folder_path_temp, file_name_nu)
            with open(src_nu_path_temp, "wb") as image:
                image.write(src_img.file.read())
            print("____path_woman___", src_nu_path_temp)
            source_face = get_one_face(cv2.imread(src_nu_path_temp))
            if source_face is None:
                os.remove(src_nu_path_temp)
                return {
                    "message": "We cannot identify the face in the photo you provided, please upload another photo"
                }

            is_duplicate = is_duplicate_image(src_nu_path_temp, folder_path_nu)
            print(is_duplicate)
            if is_duplicate:
                os.remove(src_nu_path_temp)
                print(f"{folder_path_nu}/{is_duplicate}")
                return f"{folder_path_nu}/{is_duplicate}"
            else:
                src_nu_path = os.path.join(folder_path_nu, file_name_nu)
                copy_image(src_nu_path_temp, src_nu_path)
                os.remove(src_nu_path_temp)
                print(f"{src_nu_path}")
                return f"{src_nu_path}"

        # print("pass3")
    except Exception as e:
        JSONResponse(content=({"message": f"Error: {e}", "status": 500}))


@app.post("/block/user")
async def block_user(request: Request):
    form_data = await request.form()
    user_report = form_data.get("user_report")
    block_account = form_data.get("block_account")
    report_reason = form_data.get("report_reason")

    try:

        result = (
            db.session.query(BlockUser.status)
            .filter(
                BlockUser.id_user_report == user_report,
                BlockUser.id_blocked_user == block_account,
            )
            .all()
        )
        if result:
            if result[0] == "blocked":
                return {"message": "Your account has been reported by you!!"}
            elif result[0] == "be_blocked":
                return {"message": "You have been blocked by this user!!"}

        id_rp = db.session.query(func.max(BlockUser.id_block)).scalar()
        if id_rp[0]:
            id_report = id_rp[0] + 1
        else:
            id_report = 1
        status_report = "blocked"
        status_be_report = "be_blocked"
        # new_block
        new_block = BlockUser(
            id_block=id_report,
            id_user_report=block_account,
            id_blocked_user=user_report,
            report_reason=report_reason,
            status=status_report,
        )
        # new_reverse_block_entry
        new_reverse_block_entry = BlockUser(
            id_block=id_report,
            id_user_report=block_account,
            id_blocked_user=user_report,
            report_reason=report_reason,
            status=status_be_report,
        )
        db.session.add(new_block)
        db.session.add(new_reverse_block_entry)
        db.session.commit()
        return {"message": "Successfully comment reported!"}

    except Exception as error:
        db.session.rollback()
        f"Error Exception: {error}"


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, id_user: int):
        await websocket.accept()
        websocket.id_user = id_user
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, id_user: int):
        for connection in self.active_connections:
            if int(id_user) == connection.id_user:  # Kiểm tra id_user của kết nối
                await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            print(data)
            id_user = 0
            start_index = data.find('"id_user":')
            if start_index != -1:
                # Tìm vị trí của ký tự đầu tiên sau dấu hai chấm (:)
                colon_index = data.find(":", start_index)
                # Tìm vị trí của ký tự đầu tiên sau dấu phẩy (,) hoặc dấu đóng ngoặc đơn (})
                comma_index = data.find(",", start_index)
                closing_brace_index = data.find("}", start_index)

                # Xác định vị trí kết thúc của giá trị "id_user"
                end_index = min(
                    filter(lambda x: x != -1, [comma_index, closing_brace_index])
                )

                # Trích xuất giá trị của "id_user"
                if colon_index != -1 and end_index != -1:
                    id_user = data[colon_index + 1 : end_index].strip()

            # message = {"message": data}
            await manager.broadcast(data, id_user)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"clientId": user_id, "message": "Offline"}
        await manager.broadcast(json.dumps(message), user_id)


def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username = payload.get("username")
        print(username)
        response = client.emails.send(
            From="admin@fakewedding.online",  # Địa chỉ email gửi
            To="long16072001@gmail.com",
            Subject="Swap wedding",
            TextBody="You swaped a album wedding ",
        )
    except Exception as e:
        # Handle JWT decoding error as needed
        return e


def get_data_list_sk_all_wedding():
    id_video_wedding = []
    number_album_wedding = []
    id_image_wedding = []
    count_wedding = 0
    album_wedding = 0

    # id_user = request.query_params.get("id_user")
    try:
        result_video_wedding = SavedSKVideoImageWedding.query.order_by(
            SavedSKVideoImageWedding.thoigian_sukien.desc()
        ).all()
        for row in result_video_wedding:
            video_wedding = {
                "id": row.id,
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_video_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_video_wedding.append(video_wedding)

        # Query for images wedding
        result_images_wedding = (
            SavedSuKien2Img.query.filter(SavedSuKien2Img.loai_sukien == "wedding")
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .all()
        )

        for row in result_images_wedding:
            image_data_wedding = {
                "loai_sukien": row.loai_sukien,
                "id_sk_album": row.id_sk_album,
                "album": row.album,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
            }
            id_image_wedding.append(image_data_wedding)
            count_wedding += 1
            if count_wedding == 50:
                album_wedding += 1
                count_wedding = 0
                number_album_wedding.append({"album_wedding": id_image_wedding})

        return JSONResponse(
            content={
                "sk_fake_wedding": {
                    "list_sukien_wedding_video": id_video_wedding,
                    "list_sukien_wedding_image": number_album_wedding,
                },
            }
        )
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {error}"
        )


@app.get("/get/list_2_image/id_image_swap_2face_all")
async def get_data_list_sk_all_futurelove(request: Request):
    id_video_wedding = []
    id_image_wedding = []

    id_user = request.query_params.get("id_user")
    try:
        # Query for video wedding
        result_video_wedding = (
            SavedSuKienVideo.query.filter(SavedSuKienVideo.id_user == id_user)
            .order_by(SavedSuKienVideo.thoigian_sukien.desc())
            .all()
        )

        for row in result_video_wedding:
            video_wedding = {
                # "id": row[10],
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_video_wedding.append(video_wedding)

        # Query for images wedding
        result_images_wedding = SavedSuKien2Img.query.filter(
            SavedSuKien2Img.id_user == id_user,
            SavedSuKien2Img.loai_sukien == "swap_2face",
        ).all()

        for row in result_images_wedding:
            image_data_wedding = {
                "loai_sukien": row.loai_sukien,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "thoi_gian_sk": row.thoigian_sukien,
            }
            id_image_wedding.append(image_data_wedding)

        return JSONResponse(
            content={
                "sk_future_love": {
                    "list_sukien_future_video": id_video_wedding,
                    "list_sukien_future_image": id_image_wedding,
                }
            }
        )
    except Exception as error:
        print("Error Exception", error)
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


def get_data_list_sk_all_noel():
    id_video_wedding = []
    number_album_wedding = []
    id_image_wedding = []
    count_wedding = 0
    album_wedding = 0

    # id_user = request.query_params.get("id_user")
    try:
        # Query for video wedding
        result_video_wedding = SavedSKVideoSwapImage.query.order_by(
            SavedSKVideoSwapImage.thoigian_sukien.decs()
        ).all()

        for row in result_video_wedding:
            video_wedding = {
                # "id": row[10],
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_video_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_video_wedding.append(video_wedding)

        # Query for images wedding
        result_images_wedding = SavedSuKien2Img.query.filter(
            SavedSuKien2Img.loai_sukien == "noel"
        ).all()

        for row in result_images_wedding:
            image_data_wedding = {
                "loai_sukien": row.loai_sukien,
                "id_sk_album": row.id_sk_album,
                "album": row.album,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
            }
            id_image_wedding.append(image_data_wedding)
            count_wedding += 1
            if count_wedding == 50:
                album_wedding += 1
                count_wedding = 0
                number_album_wedding.append({"album_wedding": id_image_wedding})
                id_image_wedding = []

        return JSONResponse(
            content={
                "sk_noel": {
                    "list_sukien_noel_video": id_video_wedding,
                    "list_sukien_noel_image": number_album_wedding,
                },
            }
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


def get_data_list_sk_all_growup():
    id_video_grow_up_age = []
    number_album_wedding = []
    id_image_grow_up = []
    count_wedding = 0
    album_wedding = 0

    # id_user = request.query_params.get("id_user")
    try:
        # Query for video growup
        result_video_grow_up = SavedSKVideoImageGrowup.query.order_by(
            SavedSKVideoImageGrowup.thoigian_sukien.desc()
        ).all()

        for row in result_video_grow_up:
            video_grow_up_age = {
                "id": row.id,
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_video_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_video_grow_up_age.append(video_grow_up_age)

        # Query for images growup
        result_images_wedding = SavedSuKien2Img.query.filter(
            SavedSuKien2Img.loai_sukien == "mom and baby"
        ).all()

        for row in result_images_wedding:
            image_data_wedding = {
                "loai_sukien": row.loai_sukien,
                "id_sk_album": row.id_sk_album,
                "album": row.album,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
            }
            id_image_grow_up.append(image_data_wedding)
            count_wedding += 1
            if count_wedding == 50:
                album_wedding += 1
                count_wedding = 0
                number_album_wedding.append({"album_wedding": id_image_grow_up})
                id_image_grow_up = []

        return JSONResponse(
            content={
                "sk_grow_up": {
                    "list_sukien_grow_up_video": id_video_grow_up_age,
                    "list_sukien_grow_up_image": number_album_wedding,
                },
            }
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/all_su_kien/id_user")
async def get_all_sk():
    data = []
    try:
        data_wedding = get_data_list_sk_all_wedding()
        data_futurelove = get_data_list_sk_all_futurelove()
        data_noel = get_data_list_sk_all_noel()
        data_growup = get_data_list_sk_all_growup()
        # data.append(data_wedding)
        return data_growup
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# SERVER WEDDING DATA


@app.get("/get/list_image_wedding/{album}")
async def get_data_list_image_wedding(request: Request, album: int):
    category = request.query_params.get("album")
    list_toan_bo_image = []

    try:
        result2 = ListImageWedding.query.filter(
            ListImageWedding.IDCategories == category
        ).all()
        for row in result2:
            linkImage = row.image.replace("main", "main/IMG_WEDDING")
            image = {}
            image["id"] = row.id
            image["mask"] = row.mask
            image["thongtin"] = row.thongtin
            image["image"] = linkImage
            image["dotuoi"] = row.dotuoi
            image["IDCategories"] = row.IDCategories
            list_toan_bo_image.append(image)

        return JSONResponse(content={"list_sukien_video": list_toan_bo_image})
    except Exception as error:
        print("Error Exception", error)
        return f"Error Exception: {error}"


@app.get("/get/list_image/all_wedding")
async def get_data_list_image_all():
    list_toan_bo_image = []
    try:
        result2 = ListImageWedding.query.all()
        for row in result2:
            linkImage = row.image.replace("main", "main/IMG_WEDDING")
            image = {
                "id": row.id,
                "mask": row.mask,
                "thongtin": row.thongtin,
                "image": linkImage,
                "dotuoi": row.dotuoi,
                "IDCategories": row.IDCategories,
            }
            list_toan_bo_image.append(image)

        return JSONResponse(content={"list_sukien_video": list_toan_bo_image})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/list_image_wedding/{album}")
async def get_data_list_image_wedding(request: Request, album: int):
    category = request.query_params.get("album")
    list_toan_bo_image = []

    try:
        result2 = ListImageWedding.query.filter(
            ListImageWedding.IDCategories == category
        ).all()
        for row in result2:
            linkImage = row.image.replace("main", "main/IMG_WEDDING")
            image = {
                "id": row.id,
                "mask": row.mask,
                "thongtin": row.thongtin,
                "image": linkImage,
                "dotuoi": row.dotuoi,
                "IDCategories": row.IDCategories,
            }
            list_toan_bo_image.append(image)

        return JSONResponse(content={"list_sukien_video": list_toan_bo_image})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET VIDEO WEDDING TEMPLATE


@app.get("/get/list_video/all_video_wedding_template")
async def get_data_list_video_wedding_template():
    list_toan_bo_video_wedding = []
    try:
        result2 = ListVideoWedding.query.all()

        for row in result2:
            video = {
                "id": row.id,
                "link_video": row.linkgoc,
                "noidung": row.noidung,
                "age_video": row.age_video,
                "gioitinh": row.gioitinh,
                "mau_da": row.mau_da,
                "chung_toc": row.chung_toc,
                "thumbnail": row.thumbnail,
            }
            list_toan_bo_video_wedding.append(video)
        return JSONResponse(
            content={"list_sukien_video_wedding": list_toan_bo_video_wedding}
        )

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/list_video/video_wedding_detail")
async def get_data_video_wedding_detail(request: Request):
    id = request.query_params.get("id")
    try:
        result2 = ListVideoWedding.query.filter(ListImageWedding.id == id).first()
        if result2 is None:
            return {"status": 404, "message": "Not Found ~~~~~~~~~"}
        return result2
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET ALL VIDEO SWAP
@app.get("/get/list_video/all_video_wedding_swap")
async def get_data_list_all_video_wedding_swap():
    list_toan_bo_video_wedding = []
    try:
        result2 = SavedSKVideoImageWedding.query.order_by(
            SavedSKVideoImageWedding.thoigian_sukien.desc()
        ).all()
        for row in result2:
            video = {
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_video_da_swap,
                "thoigian_sukien": row.thoigian_sukien,
                "id_user": row.id_user,
            }
            list_toan_bo_video_wedding.append(video)

        return JSONResponse(
            content={"list_sukien_video_wedding": list_toan_bo_video_wedding}
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET LIST VIDEO WEDDING THEO TIME


@app.get("/get/list_image/all_wedding_time")
async def get_data_list_video_all_wedding_swap(request: Request):
    list_toan_bo_video = []
    count = 0
    album = 0
    number_album = []
    try:
        result2 = (
            SavedSuKien2Img.query.filter(SavedSuKien2Img.loai_sukien == "wedding")
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            video = {
                "loai_sukien": row.loai_sukien,
                "id_sk_swap_album": row.id_sk_album,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "album": row.album,
                "thoigian_sukien": row.thoigian_sukien,
            }
            list_toan_bo_video.append(video)
            count += 1
            if count == 50:
                album += 1
                count = 0
                number_album.append(
                    {
                        "album": album,
                        "list_sukien_image": list_toan_bo_video,
                        "total": count,
                    }
                )
                list_toan_bo_video = []
        return JSONResponse(content=number_album)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET LIST VIDEO THEO profile của user


@app.get("/get/list_video_wedding/id_video_swap")
async def get_data_list_video_wedding_id(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        result2 = (
            SavedSKVideoImageWedding.query.filter(
                SavedSKVideoImageWedding.id_user == id_user_wedding_video
            )
            .order_by(SavedSKVideoImageWedding.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            video = {
                "id": row.id,
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_video_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_video.append(video)

        return JSONResponse(content={"list_sukien_video": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get all video swap  https://photo.gachmen.org/gensk


@app.get("/get/list_video/all_video_swap_wedding")
async def get_data_list_video_all_wedding(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        result2 = (
            SavedSKVideoImageWedding.query.filter(
                SavedSKVideoImageWedding.id_user == id_user_wedding_video
            )
            .order_by(SavedSKVideoImageWedding.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            video = {
                "id": row.id,
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_video_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_video.append(video)

        return JSONResponse(content={"list_sukien_video": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/list_video/all_video_swap_future_love")
async def get_data_list_video_all_wedding(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        result2 = (
            SavedSKVideoSwapImage.query.filter(
                SavedSKVideoSwapImage.id_user == id_user_wedding_video
            )
            .order_by(SavedSKVideoSwapImage.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            video = {
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_video_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_video.append(video)

        return JSONResponse(content={"list_sukien_video": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET SWAP VIDEO THEO ID SK
@app.get("/get/list_video/id_video_swap_all_id_sk")
async def get_data_list_video_wedding_all_id_sk(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    id_sk_wedding_image = request.query_params.get("id_sk")
    try:
        result2 = (
            SavedSKVideoImageWedding.query.filter(
                SavedSKVideoImageWedding.id_user == id_user_wedding_video,
                SavedSKVideoImageWedding.id_saved == id_sk_wedding_image,
            )
            .order_by(SavedSKVideoImageWedding.thoigian_sukien.desc())
            .all()
        )
        for row in result2:
            video = {
                "id": row.id,
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_video_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_video.append(video)
        return JSONResponse(content={"id_su_kien_swap_image": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET ALL IMAGE SWAP AND VIDEO SWAP  https://photo.gachmen.org/genvideo


@app.get("/get/list_video/all_video_image_swap_wedding")
async def get_data_list_video_image_all_futurelove(request: Request):
    id_video = []
    id_image = []
    count = 0
    album = 0
    number_album = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        # Query for video
        result_video = (
            SavedSKVideoImageWedding.query.filter(
                SavedSKVideoImageWedding.id_user == id_user_wedding_video
            )
            .order_by(SavedSKVideoImageWedding.thoigian_sukien.desc())
            .all()
        )

        for row in result_video:
            video = {
                "id": row.id,
                "id_saved": row.id_saved,
                "link_video_goc": row.link_video_goc,
                "link_image": row.link_image,
                "link_video_da_swap": row.link_video_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_video.append(video)

        # Query for images
        result_images = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.id_user == id_user_wedding_video
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .all()
        )
        for row in result_images:
            image_data = {
                "loai_sukien": row.loai_sukien,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "album": row.album,
            }
            id_image.append(image_data)
            count += 1
            if count == 50:
                album += 1
                count = 0
                number_album.append({"album": album, "list_sukien_video": id_image})
                id_image = []

        return JSONResponse(
            content={"list_sukien_video": id_video, "list_sk_image": number_album}
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get lisst image by id user sk wedding theo  profile của use


@app.get("/get/list_2_image/id_image_swap")
async def get_data_list_image_wedding_id(request: Request):
    id_image = []
    count = 0
    album = 0
    number_album = []
    id_sk_album = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        result2 = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.id_user == id_user_wedding_video,
                SavedSuKien2Img.loai_sukien == "wedding",
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .all()
        )
        # Group images by id_sk_album
        album_images = {}
        for row in result2:
            id_sk_album = row[14]
            if id_sk_album not in album_images:
                album_images[id_sk_album] = []
            video = {
                "loai_sukien": row.loai_sukien,
                "id_sk_album": row.id_sk_album,
                "album": row.album,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
            }
            album_images[id_sk_album].append(video)

        # Create albums
        for id_sk_album, images in album_images.items():
            album += 1
            number_album.append({"album": album, "list_sukien_image": images})

        return JSONResponse(content=number_album)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get lisst image by id user sk wedding theo album
@app.get("/get/list_2_image/id_image_swap_album")
async def get_data_list_image_wedding_id_album(request: Request):
    id_video = []
    id_user_wedding_video = request.query_params.get("id_user")
    id_album = request.query_params.get("album")
    try:
        result2 = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.id_user == id_user_wedding_video,
                SavedSuKien2Img.loai_sukien == "wedding",
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            video = {
                "loai_sukien": row.loai_sukien,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "album": row.album,
            }
            id_video.append(video)

        return JSONResponse(content={"list_sukien_video": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get list all sk image by id user  https://photo.gachmen.org/genimg
@app.get("/get/list_2_image/id_image_swap_all")
async def get_data_list_image_wedding_all(request: Request):
    id_image = []
    count = 0
    album = 0
    number_album = []
    id_user_wedding_video = request.query_params.get("id_user")
    try:
        result2 = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.id_user == id_user_wedding_video,
                SavedSuKien2Img.loai_sukien == "wedding",
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .all()
        )
        for row in result2:
            image = {
                "loai_sukien": row.loai_sukien,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "album": row.album,
            }
            id_image.append(image)
            count += 1
            if count == 50:
                album += 1
                count = 0
                number_album.append({"album": album, "list_sukien_video": id_image})
                id_video = []

        return JSONResponse(content=number_album)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET IMAGE SK WEDDING THEO ID SU KIEN


@app.get("/get/list_2_image/id_image_swap_all_id_sk")
async def get_data_list_image_wedding_all_id_sk(request: Request):
    id_image = []
    id_user_wedding_video = request.query_params.get("id_user")
    id_sk_wedding_image = request.query_params.get("id_sk")
    try:
        result2 = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.id_sk_album == id_sk_wedding_image,
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            image = {
                "loai_sukien": row.loai_sukien,
                "id_sk_swap_album": row.id_sk_album,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "album": row.album,
                "thoi_gian_swap": row.thoigian_swap,
            }
            id_image.append(image)
        return JSONResponse(content={"id_su_kien_swap_image": id_image})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET DETAL SK SWAP 2 image by id sk swap futurelove


@app.get("/get/list_2_image/id_image_swap_futurelove_all_id_sk")
async def get_data_list_image_wedding_futurelove_all_id_sk(request: Request):
    id_image = []
    id_user_wedding_video = request.query_params.get("id_user")
    id_sk_wedding_image = request.query_params.get("id_sk")
    try:
        result2 = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.id_saved == id_sk_wedding_image
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            image = {
                "loai_sukien": row.loai_sukien,
                "id_sk_swap_album": row.id_sk_album,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "thoi_gian_swap": row.thoigian_swap,
            }
            id_image.append(image)
        return JSONResponse(content={"id_su_kien_swap_image": id_image})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET DETAL SK SWAP image to video by id sk swap futurelove


@app.get("/get/list_video_image/id_video_swap_futurelove_all_id_sk")
async def get_data_list_image_wedding_futurelove_all_id_sk(request: Request):
    id_image = []
    id_sk_wedding_image = request.query_params.get("id_sk")
    try:
        result2 = (
            SavedSuKienVideo.query.filter(
                SavedSuKienVideo.id_saved == id_sk_wedding_image
            )
            .order_by(SavedSuKienVideo.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            image = {
                "loai_sukien": "swap video futurelove",
                "id_saved": row.id_saved,
                "link_src_goc": row.link_video_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "thoi_gian_su_kien": row.thoigian_sukien,
            }
            id_image.append(image)
        return JSONResponse(content={"id_su_kien_swap_image": id_image})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get all sk swap 2 face futurelove
@app.get("/get/list_2_image/id_image_swap_all_future_love")
async def get_data_list_image_wedding_all(request: Request):
    id_image = []
    id_user = request.query_params.get("id_user")
    try:
        result2 = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.id_user == id_user,
                SavedSuKien2Img.loai_sukien == "swap_2face",
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            image = {
                "loai_sukien": row.loai_sukien,
                "id_sk_swap_album": row.id_sk_album,
                "id_saved": row.id_saved,
                "link_src_goc": row.link_src_goc,
                "link_tar_goc": row.link_tar_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_image.append(image)

        return JSONResponse(content={"id_su_kien_swap_image": id_image})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get all sk swap baby futurelove
@app.get("/get/list_2_image/id_image_swap_baby_all_future_love")
async def get_data_list_image_wedding_all(request: Request):
    id_image = []
    id_user = request.query_params.get("id_user")
    try:
        result2 = (
            SavedSuKienSwapBaby.query.filter(SavedSuKienSwapBaby.id_user == id_user)
            .order_by(SavedSuKienSwapBaby.thoigian_sukien.desc())
            .all()
        )

        for row in result2:
            image = {
                "id_saved": row.id_saved,
                "link_nam_goc": row.link_nam_goc,
                "link_nu_goc": row.link_nu_goc,
                "link_baby_swap": row.link_baby_goc,
                "link_da_swap": row.link_da_swap,
                "id_user": row.id_user,
                "thoigian_sukien": row.thoigian_sukien,
            }
            id_image.append(image)

        return JSONResponse(content={"id_su_kien_swap_image": id_image})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# SERVER SANTA_APP
@app.get("/get/list_image/{album}")
async def get_data_list_image(request: Request, album: int):
    category = request.query_params.get("album")
    list_toan_bo_image = []

    try:
        result2 = ListImageSanta.query.filter(
            ListImageSanta.IDCategories == category
        ).all()

        for row in result2:
            image = {}
            image["id"] = row.id
            image["mask"] = row.mask
            image["thongtin"] = row.thongtin
            image["image"] = row.image
            image["dotuoi"] = row.dotuoi
            image["IDCategories"] = row.IDCategories
            list_toan_bo_image.append(image)

        return JSONResponse(content={"list_sukien_video": list_toan_bo_image})
    except Exception as error:
        return f"Error Exception: {error}"


# viet update code 17 oct 2024
@app.get("/lovehistory/listvideo/santa/{page}")
async def get_data_list_video_santa(request: Request, page: int):
    category = request.query_params.get("category")
    print(type(category))
    list_toan_bo_video = []
    thong_tin = {}
    try:
        if category == "0":
            result2 = ListVideoSantaNew.query.all()
            # print(result2)
        elif category != 0:
            result2 = ListVideoSantaNew.query.filter(
                ListVideoSantaNew.IDCategories == category
            ).all()
            # print(result2)

        # print(result2)
        soPhanTuTrenMotTrang = 50
        soTrang = (len(result2) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang
        print(len(result2))
        print(soTrang)
        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(result2))
        else:
            return JSONResponse(content="exceed the number of pages!!!")
        print("hello")
        for i in range(start, end):
            result3 = CategoriesVideo.query.filter(
                CategoriesVideo.idCateogries == result2.IDCategories
            ).first()
            thong_tin["id"] = result2[i][0]
            thong_tin["id_categories"] = result2[i][5]
            thong_tin["name_categories"] = result3[0][1]
            thong_tin["detail"] = result3[0][2]
            thong_tin["age_video"] = result2[i][6]
            thong_tin["chung_toc"] = result2[i][9]
            thong_tin["gioi_tinh"] = result2[i][7]
            thong_tin["link_video"] = result2[i][1]
            thong_tin["mau_da"] = result2[i][8]
            thong_tin["noi_dung"] = result2[i][2]
            thong_tin["thumbnail"] = result2[i][3]
            list_toan_bo_video.append(thong_tin)
            thong_tin = {}

        return JSONResponse(content={"list_sukien_video": list_toan_bo_video})
    except Exception as error:
        return f"Error Exception: {error}"


# api new by viet 17 oct 2024
@app.get("/get/santa/list_temp/{page}")
async def get_data_list_temp_santa(request: Request, page: int):
    category = request.query_params.get("category")
    print(type(category))
    list_toan_bo_video = []
    thong_tin = {}
    try:
        if category == "0":
            result2 = ListVideoSantaNew.query.all()
            # print(result2)
        elif category != 0:
            result2 = ListVideoSantaNew.query.filter(
                ListVideoSantaNew.IDCategories == category
            ).all()
            # print(result2)

        # print(result2)
        soPhanTuTrenMotTrang = 50
        soTrang = (len(result2) + soPhanTuTrenMotTrang - 1) // soPhanTuTrenMotTrang
        print(len(result2))
        print(soTrang)
        if page <= soTrang:
            start = (page - 1) * soPhanTuTrenMotTrang
            end = min(page * soPhanTuTrenMotTrang, len(result2))
        else:
            return JSONResponse(content="exceed the number of pages!!!")
        print("hello")
        for i in range(start, end):
            result3 = CategoriesVideo.query.filter(
                CategoriesVideo.idCateogries == result2.IDCategories
            ).first()
            thong_tin["id"] = result2[i][0]
            thong_tin["id_categories"] = result2[i][5]
            thong_tin["name_categories"] = result3[0][1]
            thong_tin["detail"] = result3[0][2]
            thong_tin["age_video"] = result2[i][6]
            thong_tin["chung_toc"] = result2[i][9]
            thong_tin["gioi_tinh"] = result2[i][7]
            thong_tin["link_video"] = result2[i][1]
            thong_tin["mau_da"] = result2[i][8]
            thong_tin["noi_dung"] = result2[i][2]
            thong_tin["thumbnail"] = result2[i][3]
            list_toan_bo_video.append(thong_tin)
            thong_tin = {}

        return JSONResponse(content={"list_sukien_video": list_toan_bo_video})
    except Exception as error:
        return f"Error Exception: {error}"


@app.get("/lovehistory/listimage/santa/{page}")
async def get_data_list_video_santa(request: Request, page: int):
    category = request.query_params.get("category")
    result = dict()
    # print(category)
    try:
        limit = 10
        offset = (page - 1) * limit
        if category == "0":
            data = ListImageSanta.query.limit(limit).offset(offset).all()
            data_length = len(data)
            # print(data_length)
            total_page = math.ceil(data_length / limit)

        elif category != "0":
            data = (
                ListImageSanta.query.filter(ListImageSanta.IDCategories == category)
                .limit(limit)
                .offset(offset)
                .all()
            )
            data_length = len(data)
            total_page = math.ceil(data_length / limit)

        list_image = []
        for item in data:
            info = {}
            cat_info = CategoriesVideo.query.filter(
                CategoriesVideo.idCateogries == item.IDCategories
            ).first()
            info["id"] = item[0]
            info["mask"] = item[1]
            info["name_categories"] = cat_info[0][1]
            info["detail"] = cat_info[0][2]
            info["thongtin"] = item[2]
            info["image"] = item[3]
            info["do_tuoi"] = item[4]
            info["IDCategories"] = item[5]
            list_image.append(info)

        result["data"] = list_image
        result["total_page"] = total_page
        return result
    except Exception as error:
        return f"Error Exception: {error}"


from typing import Optional


# viet update code 22 oct 2024
@app.get("/get/list_image/all_santa/{limit}")
async def get_data_list_image_all(
    request: Request, limit: int, album: Optional[int] = None
):
    list_toan_bo_image = []
    page = request.query_params.get("page", default=1)
    total_item = 0
    try:
        query_count = ListImageSanta.query.all()
        # limit = 50
        total_page = math.ceil(len(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = ListImageSanta.query.limit(limit).offset(offset).all()

        for row in result2:
            image = {
                "id": row[0],
                "mask": row[1],
                "thongtin": row[2],
                "image": row[3],
                "dotuoi": row[4],
                "IDCategories": row[5],
            }
            list_toan_bo_image.append(image)
            total_item = len(list_toan_bo_image)
        return JSONResponse(
            content={
                "list_sukien_video": list_toan_bo_image,
                "totalPage": total_page,
                "totalItem": total_item,
                "currentPage": int(page),
            }
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/list_video/all_santa/{limit}")
async def get_data_list_video_all(request: Request, limit: int):
    list_toan_bo_video = []
    page = request.query_params.get("page", default=1)
    total_item = 0
    try:
        query_count = ListVideoSanta.query.all()
        # limit = 50
        total_page = math.ceil(len(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = ListVideoSanta.query.limit(limit).offset(offset).all()

        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "IDCategories": row[3],
                "age_video": row[4],
                "gioitinh": row[5],
                "mau_da": row[6],
                "chung_toc": row[7],
            }
            list_toan_bo_video.append(video)
            total_item = len(list_toan_bo_video)

        return JSONResponse(
            content={
                "list_sukien_video": list_toan_bo_video,
                "totalPage": total_page,
                "totalItem": total_item,
                "currentPage": int(page),
            }
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/list_video/id_santa")
async def get_data_list_video_id(request: Request):
    id_video = []
    id_video_santa = request.query_params.get("id_video_santa")
    try:
        result2 = ListVideoSanta.query.filter_by(id=id).all()
        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "IDCategories": row[3],
                "age_video": row[4],
                "gioitinh": row[5],
                "mau_da": row[6],
                "chung_toc": row[7],
            }
            id_video.append(video)

        return JSONResponse(content={"list_sukien_video": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get video, image theo id user


@app.get("/get/id_video/id_user")
async def get_data_list_video_id(request: Request):
    id_video = []
    id_user = request.query_params.get("id_user")
    try:
        result2 = SavedSuKienVideo.query.filter(
            SavedSuKienVideo.id_user == id_user
        ).all()

        for row in result2:
            video = {
                "id_saved": row[0],
                "link_video": row[1],
                "link_image": row[2],
                "link_da_swap": row[3],
                "ten_su_kien": row[4],
                "noidung_su_kien": row[5],
                "id_video": row[6],
                "id_user": row[10],
            }
            id_video.append(video)

        return JSONResponse(content={"list_sukien_video": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/id_image/id_user")
async def get_data_list_video_id(request: Request):
    id_image = []
    id_user = request.query_params.get("id_user")
    try:
        result2 = SavedSuKien2Img.query.filter(SavedSuKien2Img.id_user == id_user).all()

        for row in result2:
            image = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[8],
            }
            id_image.append(image)

        return JSONResponse(content={"list_sukien_video": id_image})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get thong tin album image


@app.get("/get/list_album")
async def get_data_list_video_id(request: Request):
    id_album = []
    server = request.query_params.get("server")
    try:
        result2 = ListAlbum.query.filter(ListAlbum.server == server).all()

        for row in result2:
            album = {
                "id ": row[0],
                "noidung": row[1],
                "id_album": row[2],
                "server": row[3],
                "thumpImage": row[4],
            }
            id_album.append(album)

        return JSONResponse(content={"list_sukien_video": id_album})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/list_album/id_album")
async def get_data_list_video_id(request: Request):
    id_album = []
    server = request.query_params.get("server")
    id = request.query_params.get("id")
    try:
        result2 = ListAlbum.query.filter(
            ListAlbum.server == server, ListAlbum.id_album == id
        ).all()
        for row in result2:
            album = {
                "id ": row[0],
                "noidung": row[1],
                "id_album": row[2],
                "server": row[3],
            }
            id_album.append(album)

        return JSONResponse(content={"list_sukien_video": id_album})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/list_video/all_video_baby_mom", tags=["list_video"])
async def get_data_list_video_all(request: Request):
    list_temp = dict()
    page = request.query_params.get("page")
    if page == None:
        page = "1"
    try:
        limit = 10
        offset = (int(page) - 1) * limit
        query = ListVideoBaby.query.all()
        total_page = math.ceil(len(query) / limit)
        result2 = ListVideoBaby.query.limit(limit).offset(offset).all()

        temp = []
        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "gioitinh": row[7],
                "mau_da": row[8],
                "chung_toc": row[9],
            }
            temp.append(video)
        list_temp["data"] = temp
        list_temp["total_page"] = total_page

        return list_temp
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/list_image/mom_baby_temp_detail", tags=["list_image"])
async def get_mom_baby_temp_detail(request: Request):
    list_image = []
    try:
        id_cate = request.query_params.get("id")
        result2 = ListImageMotherBaby.query.filter(
            ListImageMotherBaby.IDCategories == id_cate
        ).all()
        for row in result2:
            data = {
                "id": row[0],
                "mask": row[1],
                "thongtin": row[2],
                "image": row[3],
                "dotuoi": row[4],
                "IDCategories": row[5],
            }
            list_image.append(data)

        return list_image
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/get/list_video/id_video", tags=["list_video"])
async def get_data_list_video_id(request: Request):
    id_video = []
    id_video_santa = request.query_params.get("id_video")
    try:
        result2 = ListVideo.query.filter_by(id=id_video_santa).all()

        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "IDCategories": row[3],
                "age_video": row[4],
                "gioitinh": row[5],
                "mau_da": row[6],
                "chung_toc": row[7],
            }
            id_video.append(video)

        return JSONResponse(content={"list_sukien_video": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET ALL VIDEO SWAP


@app.get("/get/list_video/all_video_swap", tags=["list_video"])
async def get_data_list_video_all_swap(request: Request):
    list_toan_bo_video = []
    try:
        result2 = SavedSKVideoImageGrowup.query.all()

        for row in result2:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
            }
            list_toan_bo_video.append(video)

        return JSONResponse(content={"list_sukien_video": list_toan_bo_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET VIDEO SWAP THEO ID
@app.get("/get/list_video/id_video_swap", tags=["list_video"])
async def get_data_list_video_id(request: Request):
    id_video = []
    id_video_santa = request.query_params.get("id_video_swap")
    try:
        result2 = SavedSKVideoImageGrowup.query.filter(
            SavedSKVideoImageGrowup.id == id_video_santa
        ).all()

        for row in result2:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
            }
            id_video.append(video)

        return JSONResponse(content={"list_sukien_video": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET VIDEO SWAP  THEO ID USER
@app.get("/get/list_video/id_user_swap", tags=["list_video"])
async def get_data_list_video_mom_baby_id(request: Request):
    id_video = []
    id_user = request.query_params.get("id_user")
    try:
        result2 = SavedSKVideoImageGrowup.query.filter(
            SavedSKVideoImageGrowup.id_user == id_user
        ).all()
        for row in result2:
            video = {
                "id": row[10],
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "id_user": row[7],
            }
            id_video.append(video)

        return JSONResponse(content={"list_sukien_video": id_video})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET album SWAP IMAGE THEO ALBUM
@app.get("/get/list_video/id_image_album_swap", tags=["list_video"])
async def get_data_list_swap_image_album(request: Request):
    id_image = []
    album_mom_baby = request.query_params.get("album")
    try:
        result2 = SavedSKVideoImageGrowup.query.filter(
            SavedSKVideoImageGrowup.id == album_mom_baby
        ).all()
        print(result2)
        for row in result2:
            video = {
                "id": row[10],
                "album": row[10],
                "id_saved": row[0],
                "link_mom_goc": row[1],
                "link_baby_goc": row[2],
                "link_da_swap": row[3],
                "id_user": row[7],
            }
            id_image.append(video)

        return JSONResponse(content={"list_sukien_video": id_image})
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/list_image/all_image_swap", tags=["list_image"])
async def get_data_list_swap_image_album(request: Request):
    id_image = []
    id_user = request.query_params.get("id_user")
    type = request.query_params.get("type")
    try:
        result2 = SavedSuKien2Img.query.filter(
            SavedSuKien2Img.id_user == id_user,
            SavedSuKien2Img.loai_sukien.ilike(f"%{type}%"),
        ).all()
        for row in result2:
            link_da_swap = row[3].replace(
                "https://futurelove.online", "https://photo.gachmen.org"
            )
            data = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_tar_goc": row[2],
                "link_da_swap": link_da_swap,
                "id_toan_bo_su_kien": row[4],
                "thoigian_sukien": row[5],
                "device_them_su_kien": row[6],
                "ip_them_su_kien": row[7],
                "id_user": row[8],
                "count_comment": row[9],
                "count_view": row[10],
                "id_template": row[11],
                "loai_sukien": row[12],
                "album": row[13],
                "id_sk_album": row[14],
            }
            id_image.append(data)

        return id_image
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/list_image/all_image_swap_mom_baby", tags=["list_image"])
async def get_data_list_swap_image_album(request: Request):
    id_image = []
    id_user = request.query_params.get("id_user")
    type = request.query_params.get("type")
    try:
        result2 = SavedSuKienAlone.query.filter(
            SavedSuKienAlone.id_user == id_user,
            SavedSuKienAlone.loai_sukien.ilike(f"%{type}%"),
        ).all()
        for row in result2:
            link_da_swap = row[2].replace(
                "https://futurelove.online", "https://photo.gachmen.org"
            )
            data = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_da_swap": link_da_swap,
                "id_toan_bo_su_kien": row[3],
                "thoigian_sukien": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "id_template": row[10],
                "loai_sukien": row[11],
                "album": row[12],
                "id_sk_album": row[13],
            }
            id_image.append(data)

        return id_image
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


@app.get("/list_image/all_image_swap_generate", tags=["list_image"])
async def get_data_list_swap_image_album(request: Request):
    id_image = []
    id_user = request.query_params.get("id_user")
    try:
        result2 = SavedSuKienSwapBaby.query.filter(
            SavedSuKienSwapBaby.id_user == id_user
        ).all()
        for row in result2:
            link_da_swap = row[4].replace(
                "https://futurelove.online", "https://photo.gachmen.org"
            )
            data = {
                "id_saved": row[0],
                "link_nam_goc": row[1],
                "link_nu_goc": row[2],
                "link_baby_goc": row[3],
                "link_da_swap": link_da_swap,
                "id_toan_bo_su_kien": row[5],
                "noi_dung_su_kien": row[6],
                "thoigian_sukien": row[7],
                "device_them_su_kien": row[8],
                "ip_them_su_kien": row[9],
                "id_user": row[10],
                "tomLuocText": row[11],
                "count_comment": row[12],
                "count_view": row[13],
                "id_template": row[14],
            }
            id_image.append(data)

        return id_image
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET ALL VIDEO GROW UP


@app.get("/get/list_video/all_video", tags=["list_video"])
async def get_data_list_video_all(request: Request):
    type_video = request.query_params.get("type_video")
    list_toan_bo_video = []
    try:
        result2 = ListVideo.query.filter(
            ListVideo.noidung.ilike(f"%{type_video}%")
        ).all()

        for row in result2:
            video = {
                "id": row[0],
                "linkgoc": row[1],
                "noidung": row[2],
                "gioitinh": row[7],
                "mau_da": row[8],
                "chung_toc": row[9],
            }
            list_toan_bo_video.append(video)

        return JSONResponse(content={"list_sukien_video": list_toan_bo_video})
    except Exception as error:
        print("pass Error")
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get list newborn, time machine, dad and mom
@app.get("/get/list_all_newborn/{id_user}", tags=["list_all_newborn"])
async def get_list_all_newborn(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSuKien2Img.query.filter(
            SavedSuKien2Img.loai_sukien == "newborn", SavedSuKien2Img.id_user == id_user
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.loai_sukien == "newborn",
                SavedSuKien2Img.id_user == id_user,
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.asc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            link_src_goc = row[1].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            link_da_swap = row[3].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            link_tar_goc = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_src_goc": link_src_goc,
                "link_da_swap": link_da_swap,
                "link_tar_goc": link_tar_goc,
                "id_toan_bo_su_kien": row[4],
                # "thoigian_sukien": row[5],
                # "device_them_su_kien": row[6],
                # "ip_them_su_kien": row[7],
                "id_user": row[8],
                "count_comment": row[9],
                "count_view": row[10],
                # "id_template": row[11],
                "loai_sukien": row[12],
                # "album": row[13],
                # "id_sk_album": row[14],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/list_all_time_machine/{id_user}", tags=["list_all_timeMachine"])
async def get_list_all_timeMachine(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSKVideoImageGrowup.query.filter_by(id_user=id_user).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSKVideoImageGrowup.query.filter_by(id_user=id_user)
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.asc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/list_all_dadandmom/{id_user}", tags=["list_all_dadandmom"])
async def get_list_all_dadandmom(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSKVideoSwapImage.query.filter_by(id_user=id_user).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSKVideoSwapImage.query.filter_by(id_user=id_user)
            .order_by(SavedSKVideoSwapImage.id.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/list_all_time_machine/{id_user}", tags=["list_all_time_machine"])
async def get_list_all_time_machine(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSKVideoImageGrowup.query.filter(
            SavedSKVideoImageGrowup.id_user == id_user,
            SavedSKVideoImageGrowup.loai_sk.not_(
                [
                    "baby_catwalk",
                    "baby_funny",
                    "baby_hallowen",
                    "model",
                    "baby_future_love",
                ]
            ),
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_user == id_user,
                SavedSKVideoImageGrowup.loai_sk.not_(
                    [
                        "baby_catwalk",
                        "baby_funny",
                        "baby_hallowen",
                        "model",
                        "baby_future_love",
                    ]
                ),
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        for row in result2:
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": row[2],
                "link_video_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get all su kien
@app.get("/get/list_all_sk/{id_sukien}", tags=["list_all_sk"])
async def get_list_all_sk(request: Request, id_sukien: int):
    list_all_sk = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSuKien.query.filter(
            SavedSuKien.id_toan_bo_su_kien == id_sukien
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSuKien.query.filter(SavedSuKien.id_toan_bo_su_kien == id_sukien)
            .order_by(SavedSuKien.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_save": row[0],
                "ten_nam": row[16],
                "link_nam_goc": row[1],
                "ten_nu": row[17],
                "link_nu_goc": row[2],
                "link_nam_chua_swap": row[3],
                "link_nu_chua_swap": row[4],
                "link_da_swap": row[5],
                "thoigian_swap": row[6],
                "ten_su_kien": row[7],
                "noidung_su_kien": row[8],
                "id_toan_bo_su_kien": row[9],
                "so_thu_tu_su_kien": row[10],
                "thoigian_sukien": row[11],
                "id_user": row[14],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
        return JSONResponse(
            content={
                "list_all_sk": list_all_sk,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get all mom and kid
@app.get("/get/list_all_kidandmom/{id_user}", tags=["list_all_kidandmom"])
async def get_list_all_kidandmom(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSuKienAlone.query.filter(
            SavedSuKien.id_user == id_user
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSuKienAlone.query.filter(SavedSuKien.id_user == id_user)
            .order_by(SavedSuKien.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_src_goc": row[1],
                "link_da_swap": row[2],
                "id_toan_bo_su_kien": row[3],
                "thoigian_sukien": row[4],
                # "device_them_su_kien": row[5],
                # "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                # "id_itemplate": row[10],
                "loai_sk": row[11],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
        return JSONResponse(
            content={
                "list_data": list_all_sk,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get list generator
@app.get("/get/list_all_generator/{id_user}", tags=["list_all_generator"])
async def get_list_all_generator(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSuKienSwapBaby.query.filter_by(id_user=id_user).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSuKienSwapBaby.query.filter_by(id_user=id_user)
            .order_by(SavedSuKienSwapBaby.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_nam_goc": row[1],
                # "link_nu_goc": row[2],
                # "link_baby_goc ": row[3],
                "link_da_swap": row[4],
                "id_toan_bo_su_kien": row[5],
                # " noi_dung_su_kien ": row[6],
                # "thoigian_sukien": row[7],
                "id_user": row[10],
                "tomLuocText": row[11],
                "count_comment": row[12],
                "count_view": row[13],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
        return JSONResponse(
            content={
                "list_data": list_all_sk,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get detail
@app.get("/get/detail/newborn/{id_saved}", tags=["detail_newborn"])
async def detail_newborn(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        result2 = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.loai_sukien == "newborn",
                SavedSuKien2Img.id_saved == id_saved,
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.asc())
            .all()
        )

        for row in result2:
            data = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_da_swap": row[2],
                "link_tar_goc": row[3],
                "id_toan_bo_su_kien": row[4],
                "thoigian_sukien": row[5],
                "device_them_su_kien": row[6],
                "ip_them_su_kien": row[7],
                "id_user": row[8],
                "count_comment": row[9],
                "count_view": row[10],
                "id_template": row[11],
                "loai_sukien": row[12],
                "album": row[13],
                "id_sk_album": row[14],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_detail": list_data,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/detail/time_machine/{id_saved}", tags=["detail_timeMachine"])
async def detail_timeMachine(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_saved == id_saved,
                SavedSKVideoImageGrowup.loai_sk.not_(
                    [
                        "baby_catwalk",
                        "baby_funny",
                        "baby_hallowen",
                        "model",
                        "baby_future_love",
                    ]
                ),
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.asc())
            .all()
        )
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_detail": list_data,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/detail/dadandmom/{id_saved}", tags=["detail_dadandmom"])
async def detail_dadandmom(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        result2 = (
            SavedSuKienSwapBaby.query.filter(SavedSuKienSwapBaby.id_saved == id_saved)
            .order_by(SavedSuKienSwapBaby.thoigian_sukien, desc())
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_nam_goc": row[1],
                "link_nu_goc": row[2],
                "link_baby_goc": row[3],
                "link_da_swap": row[4],
                "id_toan_bo_su_kien": row[5],
                "noi_dung_su_kien": row[6],
                "thoigian_sukien": row[7],
                "device_them_su_kien": row[8],
                "ip_them_su_kien": row[9],
                "id_user": row[10],
                "tomLuocText": row[11],
                "count_comment": row[12],
                "count_view": row[13],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/detail/kidandmom/{id_saved}", tags=["detail_kidandmom"])
async def get_list_detail_kidandmom(request: Request, id_saved: int):
    list_detail = []
    total_item = 0
    try:
        result2 = (
            SavedSuKienAlone.query.filter(SavedSuKienAlone.id_saved == id_saved)
            .order_by(SavedSuKienAlone.thoigian_sukien.desc())
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_src_goc": row[1],
                "link_da_swap": row[2],
                "id_toan_bo_su_kien": row[3],
                "thoigian_sukien": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "id_itemplate": row[10],
                "loai_sk": row[11],
            }
            list_detail.append(data)
            total_item = len(list_detail)
        return JSONResponse(
            content={
                "list_data": list_detail,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/detail/generator/{id_saved}", tags=["detail_generator"])
async def detail_generator(request: Request, id_saved: int):
    list_detail = []
    total_item = 0
    try:
        result2 = (
            SavedSuKienSwapBaby.query.filter(SavedSuKienSwapBaby.id_saved == {id_saved})
            .order_by(SavedSuKienSwapBaby.thoigian_sukien.desc())
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_nam_goc": row[1],
                "link_nu_goc": row[2],
                "link_baby_goc ": row[3],
                "link_da_swap": row[4],
                "id_toan_bo_su_kien": row[5],
                " noi_dung_su_kien ": row[6],
                "thoigian_sukien": row[7],
                "id_user": row[10],
                "tomLuocText": row[11],
                "count_comment": row[12],
                "count_view": row[13],
            }
            list_detail.append(data)
            total_item = len(list_detail)
        return JSONResponse(
            content={
                "list_data": list_detail,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to MySQL database: {e}"
        )


# API NEW BABY
# get list detail category baby catwalk
@app.get(
    "/get/baby_catwalk/detail_category/{id}", tags=["detail_category_baby_catwalk"]
)
async def get_detail_category_baby_catwalk(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        result2 = ListVideoCatwalk.query.filter(
            ListVideoCatwalk.IDCategories == id
        ).all()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
        return JSONResponse(
            content={
                "list_all_category": list_detail_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get list category baby funny
@app.get("/get/baby_funny/detail_category/{id}", tags=["detail_category_baby_funny"])
async def get_detail_category_baby_funny(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        result2 = ListVideoBabyFunny.query.filter(
            ListVideoBabyFunny.IDCategories == id
        ).all()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
        return JSONResponse(
            content={
                "list_detail_category": list_detail_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get list category baby hallowen
@app.get(
    "/get/baby_hallowen/detail_category/{id}", tags=["detail_category_baby_hallowen"]
)
async def get_detail_category_baby_hallowen(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        result2 = ListVideoHallowen.query.filter(
            ListVideoHallowen.IDCategories == id
        ).all()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
        return JSONResponse(
            content={
                "list_detail_category": list_detail_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get list category baby model
@app.get("/get/model/detail_category/{id}", tags=["detail_category_model"])
async def get_detail_category_model(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        result2 = ListVideoModel.query.filter(ListVideoModel.IDCategories == id).all()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
        return JSONResponse(
            content={
                "list_detail_category": list_detail_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get list category baby future love
@app.get(
    "/get/baby_future_love/detail_category/{id}",
    tags=["detail_category_baby_future_love"],
)
async def get_detail_category_baby_future_love(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        result2 = ListVideoBabyFuture.query.filter(
            ListVideoBabyFuture.IDCategories == id
        ).all()
        for row in result2:
            data = {
                "id": row[0],
                "image_URL": row[1],
                "name_category": row[2],
                "image_thumnail": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
        return JSONResponse(
            content={
                "list_detail_category": list_detail_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get all baby catwalk
@app.get("/get/list_all_baby_catwalk/{id_user}", tags=["list_all_baby_catwalk"])
async def get_list_all_baby_catwalk(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSKVideoImageGrowup.query.filter(
            SavedSKVideoImageGrowup.id_user == id_user,
            SavedSKVideoImageGrowup.loai_sk == "baby_catwalk",
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_user == id_user,
                SavedSKVideoImageGrowup.loai_sk == "baby_catwalk",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get all baby funny
@app.get("/get/list_all_baby_funny/{id_user}", tags=["list_all_baby_funny"])
async def get_list_all_baby_funny(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSKVideoImageGrowup.query.filter(
            SavedSKVideoImageGrowup.id_user == id_user,
            SavedSKVideoImageGrowup.loai_sk == "baby_funny",
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_user == id_user,
                SavedSKVideoImageGrowup.loai_sk == "baby_funny",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# get all baby hallowen
@app.get("/get/list_all_baby_hallowen/{id_user}", tags=["list_all_baby_hallowen"])
async def get_list_all_baby_hallowen(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSKVideoImageGrowup.query.filter(
            SavedSKVideoImageGrowup.id_user == id_user,
            SavedSKVideoImageGrowup.loai_sk == "baby_hallowen",
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_user == id_user,
                SavedSKVideoImageGrowup.loai_sk == "baby_hallowen",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get all model
@app.get("/get/list_all_model/{id_user}", tags=["list_all_model"])
async def get_list_all_model(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSKVideoImageGrowup.query.filter(
            SavedSKVideoImageGrowup.id_user == id_user,
            SavedSKVideoImageGrowup.loai_sk == "model",
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_user == id_user,
                SavedSKVideoImageGrowup.loai_sk == "model",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get all baby future_love
@app.get("/get/list_all_baby_future_love/{id_user}", tags=["list_all_baby_future_love"])
async def get_list_all_baby_future_love(request: Request, id_user: int):
    list_data = []
    page = request.query_params.get("page")
    total_item = 0
    try:
        query_count = SavedSKVideoImageGrowup.query.filter(
            SavedSKVideoImageGrowup.id_user == id_user,
            SavedSKVideoImageGrowup.loai_sk == "baby_future_love",
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_user == id_user,
                SavedSKVideoImageGrowup.loai_sk == "baby_future_love",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image": row[2],
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_tao_vid": row[5],
                # "ip_tao_vid": row[6],
                "id_user": row[7],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_data": list_data,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# detail baby_catwalk
@app.get("/get/detail/baby_catwalk/{id_saved}", tags=["detail_baby_catwalk"])
async def detail_baby_catwalk(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_saved == id_saved,
                SavedSKVideoImageGrowup.loai_sk == "baby_catwalk",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .first()
        )
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_detail": list_data,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# detail baby_funny
@app.get("/get/detail/baby_funny/{id_saved}", tags=["detail_baby_funny"])
async def detail_baby_funny(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_saved == id_saved,
                SavedSKVideoImageGrowup.loai_sk == "baby_funny",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .first()
        )
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_detail": list_data,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# detail baby_hallowen
@app.get("/get/detail/baby_hallowen/{id_saved}", tags=["detail_baby_hallowen"])
async def detail_baby_hallowen(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_saved == id_saved,
                SavedSKVideoImageGrowup.loai_sk == "baby_hallowen",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .first()
        )
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_detail": list_data,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# detail model
@app.get("/get/detail/model/{id_saved}", tags=["detail_model"])
async def detail_model(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_saved == id_saved,
                SavedSKVideoImageGrowup.loai_sk == "model",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .first()
        )
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_detail": list_data,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# detail baby_future_love
@app.get("/get/detail/baby_future_love/{id_saved}", tags=["detail_baby_future_love"])
async def detail_baby_future_love(request: Request, id_saved: int):
    list_data = []
    total_item = 0
    try:
        result2 = (
            SavedSKVideoImageGrowup.query.filter(
                SavedSKVideoImageGrowup.id_saved == id_saved,
                SavedSKVideoImageGrowup.loai_sk == "baby_future_love",
            )
            .order_by(SavedSKVideoImageGrowup.thoigian_sukien.desc())
            .first()
        )
        for row in result2:
            link_image = row[2].replace(
                "/var/www/build_futurelove/", "https://photo.gachmen.org/"
            )
            data = {
                "id_saved": row[0],
                "link_video_goc": row[1],
                "link_image": link_image,
                "link_vid_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_tao_vid": row[5],
                "ip_tao_vid": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_data.append(data)
            total_item = len(list_data)
        return JSONResponse(
            content={
                "list_detail": list_data,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# API FANCY
# get list category fancy ai


@app.get("/get/fancy/category", tags=["list_category_fancyAI"])
async def get_list_category_fancyAI(request: Request):
    list_all_category = []
    total_item = 0
    try:
        result2 = ListImageFancyAI.query.distinct(
            ListImageFancyAI.IDCategories, ListImageFancyAI.thongtin
        ).all()
        for row in result2:
            data = {
                "id": row[0],
                "name_category": row[1],
            }
            list_all_category.append(data)
            total_item = len(list_all_category)
        return JSONResponse(
            content={
                "list_all_category": list_all_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/fancy/detail_category/{id}", tags=["list_detail_category_fancyAI"])
async def get_list_detail_category_fancyAI(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        result2 = ListImageFancyAI.query.filter_by(IDCategories=id).first()
        for row in result2:
            data = {"id": row[5], "name_category": row[2], "image_URL": row[3]}
            list_detail_category.append(data)
            total_item = len(list_detail_category)
        return JSONResponse(
            content={
                "list_detail_category": list_detail_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get detail swap fancy ai
@app.get("/get/detail/fancy_ai/{id_saved}", tags=["detail_fancy_ai"])
async def detail_fancy_ai(request: Request, id_saved: int):
    list_detail = []
    total_item = 0
    try:
        result2 = SavedSuKienAlone.query.filter_by(id_saved=id_saved).first()
        for row in result2:
            data = {
                "id_saved": row[0],
                "link_goc": row[1],
                "link_da_swap": row[2],
                "id_toan_bo_su_kien": row[3],
                " thoigian_sukien ": row[4],
                "device_them_su_kien": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_detail.append(data)
            total_item = len(list_detail)
        return JSONResponse(
            content={
                "list_data": list_detail,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get all swap fancy ai
@app.get("/get/list_all_fancy_ai/{id_user}", tags=["list_all_fancy_ai"])
async def get_list_all_fancy_ai(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page", default=1)
    total_item = 0
    try:
        query_count = SavedSuKienAlone.query.filter(
            SavedSuKienAlone.id_user == id_user,
            SavedSuKienAlone.loai_sukien == "fancy_face",
        ).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSuKienAlone.query.filter(
                SavedSuKienAlone.id_user == id_user,
                SavedSuKienAlone.loai_sukien == "fancy_face",
            )
            .order_by(SavedSuKienAlone.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_src_goc": row[1],
                "link_da_swap": row[2],
                "id_toan_bo_su_kien": row[3],
                "thoigian_sukien": row[4],
                # "device_them_su_kien": row[5],
                # "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                # "id_itemplate": row[10],
                "loai_sk": row[11],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
        return JSONResponse(
            content={
                "list_data": list_all_sk,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get list video category fancy mebau
@app.get("/get/fancy/detail_category/mebau/{id}", tags=["list_detail_category_mebau"])
async def get_list_detail_category_mebau(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        result2 = ListVideoMebau.query.filter_by(IDCategories=id).all()
        for row in result2:
            data = {"id": row[5], "name_category": row[3], "image_URL": row[2]}
            list_detail_category.append(data)
            total_item = len(list_detail_category)
        return JSONResponse(
            content={
                "list_all_category": list_detail_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get detail fancy mebau
@app.get("/get/detail/fancy_mebau/{id_saved}", tags=["detail_fancy_mebau"])
async def detail_fancy_mebau(request: Request, id_saved: int):
    list_detail = []
    total_item = 0
    try:
        result2 = SavedSKVideoImageMeBau.query.filter_by(id_saved=id_saved).first()
        for row in result2:
            data = {
                "id_saved": row[0],
                "id": row[10],
                "link_video_goc": row[1],
                "link_image ": row[2],
                "link_video_da_swap": row[3],
                "thoigian_sukien": row[4],
                "device_them_su_kien ": row[5],
                "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_detail.append(data)
            total_item = len(list_detail)
        return JSONResponse(
            content={
                "list_data": list_detail,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get all swap video fancy mebau
@app.get(
    "/get/list_all_swap_video_fancy_mebau/{id_user}",
    tags=["list_all_video_fancy_mebau"],
)
async def get_list_all_video_fancy_mebau(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page", default=1)
    total_item = 0
    try:
        query_count = SavedSKVideoImageMeBau.query.filter_by(id_user=id_user).count()
        limit = 50
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSKVideoImageMeBau.query.filter_by(id_user=id_user)
            .order_by(SavedSKVideoImageMeBau.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_video_goc": row[1],
                # "link_image_goc": row[2],
                "link_da_swap": row[3],
                "thoigian_sukien": row[4],
                # "device_them_su_kien": row[5],
                # "ip_them_su_kien": row[6],
                "id_user": row[7],
                "count_comment": row[8],
                "count_view": row[9],
                "loai_sk": row[11],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
        return JSONResponse(
            content={
                "list_data": list_all_sk,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/fancy_mebau/category", tags=["list_category_fancyMeBau"])
async def get_list_category_fancyMeBau(request: Request):
    list_all_category = []
    total_item = 0
    try:
        result2 = ListImagePreg.query.distinct(
            ListImagePreg.IDCategories, ListImagePreg.thongtin
        ).all()
        for row in result2:
            data = {
                "id": row[0],
                "name_category": row[1],
            }
            list_all_category.append(data)
            total_item = len(list_all_category)
        return JSONResponse(
            content={
                "list_all_category": list_all_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# api detail category fancy mebau
@app.get("/get/fancy_mebau/detail_category/{id}", tags=["list_category_fancyMeBau"])
async def get_list_detail_category_fancyMeBau(request: Request, id: int):
    list_detail_category = []
    total_item = 0
    try:
        result2 = ListImagePreg.query.filter_by(IDCategories=id).all()
        for row in result2:
            data = {
                "id": row[0],
                "name_category": row[2],
                "image_URL": row[3],
                "idCategory": row[5],
            }
            list_detail_category.append(data)
            total_item = len(list_detail_category)
        return JSONResponse(
            content={
                "list_detail_category": list_detail_category,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# api swap 2 image fancy me bau
@app.get(
    "/get/list_all_swap_2image_fancy_mebau/{id_user}",
    tags=["list_all_2image_fancy_mebau"],
)
async def get_list_all_2image_fancy_mebau(request: Request, id_user: int):
    list_all_sk = []
    page = request.query_params.get("page", default=1)
    total_item = 0
    try:

        query_count = SavedSuKien2Img.query.filter(
            SavedSuKien2Img.id_user == id_user,
            SavedSuKien2Img.loai_sukien == "baby_fancy",
        ).count()
        limit = 20
        total_page = math.ceil(int(query_count) / limit)
        offset = (int(page) - 1) * limit
        result2 = (
            SavedSuKien2Img.query.filter(
                SavedSuKien2Img.id_user == id_user,
                SavedSuKien2Img.loai_sukien == "baby_fancy",
            )
            .order_by(SavedSuKien2Img.thoigian_sukien.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        for row in result2:
            data = {
                "id_saved": row[0],
                # "link_goc_image1": row[1],
                # "link_goc_image2": row[2],
                "link_da_swap": row[3],
                "id_toan_bo_su_kien": row[4],
                "thoigian_sukien": row[5],
                # "device_them_su_kien": row[6],
                # "ip_them_su_kien": row[7],
                "id_user": row[8],
                "count_comment": row[9],
                "count_view": row[10],
                # "id_template": row[11],
                "loai_sk": row[12],
                # "id_sk_album": row[14],
            }
            list_all_sk.append(data)
            total_item = len(list_all_sk)
        return JSONResponse(
            content={
                "list_data": list_all_sk,
                "status": 200,
                "total_item": total_item,
                "total_page": total_page,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# get detail fancy mebau
@app.get(
    "/get/detail/fancy_mebau_2image/{id_saved}", tags=["detail_fancy_mebau_2image"]
)
async def detail_fancy_mebau_2image(request: Request, id_saved: int):
    list_detail = []
    total_item = 0
    try:
        result2 = SavedSuKien2Img.query.filter(
            SavedSuKien2Img.id_saved == id_saved,
            SavedSuKien2Img.loai_sukien == "baby_fancy",
        ).first()
        for row in result2:
            data = {
                "id_saved": row[0],
                "id": row[10],
                "link_src_goc": row[1],
                "link_tar_goc ": row[2],
                "link_da_swap": row[3],
                "id_toan_bo_su_kien": row[4],
                "thoigian_sukien": row[5],
                "device_them_su_kien ": row[6],
                "ip_them_su_kien": row[7],
                "id_user": row[8],
                "count_comment": row[9],
                "count_view": row[10],
                "loai_sk": row[12],
                "id_album_sk": row[14],
            }
            list_detail.append(data)
            total_item = len(list_detail)
        return JSONResponse(
            content={
                "list_data": list_detail,
                "status": 200,
                "total_item": total_item,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# App Bikini
@app.get("/get/list_image_bikini/{album}")
async def get_data_list_image_bikini(request: Request, album: int):
    category = request.query_params.get("album")
    list_toan_bo_image = []

    try:
        result2 = ListImageBikini.query.filter_by(IDCategories=album).all()

        for row in result2:
            image = {}
            image["id"] = row[0]
            image["mask"] = row[1]
            image["thongtin"] = row[2]
            image["image"] = row[3]
            image["dotuoi"] = row[4]
            image["IDCategories"] = row[5]
            list_toan_bo_image.append(image)

        return JSONResponse(content={"list_sukien_video": list_toan_bo_image})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


@app.get("/get/list_image/all_bikini/{album}")
async def get_data_list_image_all(album: Optional[int] = None):
    list_toan_bo_image = []
    try:
        result2 = ListImageBikini.query.all()

        for row in result2:
            image = {
                "id": row[0],
                "mask": row[1],
                "thongtin": row[2],
                "image": row[3],
                "dotuoi": row[4],
                "IDCategories": row[5],
            }
            list_toan_bo_image.append(image)

        return JSONResponse(content={"list_sukien_video": list_toan_bo_image})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Exception: {e}")


# run app

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run("server_fast:app", host="0.0.0.0", port=9090)
    uvicorn.run("server_fast:app", host="0.0.0.0", port=9000)
