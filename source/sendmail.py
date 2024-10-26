import datetime
import re
from typing import Union, Any
import asyncio
import jwt
import random
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import binascii
import os
from postmarker.core import PostmarkClient
from datetime import datetime, timedelta
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydantic import BaseModel, EmailStr
import cv2
from email.message import EmailMessage
from sqlalchemy import func, desc, or_
from source import db

binascii.hexlify(os.urandom(24))

from os import environ as env
from email.mime.text import MIMEText
import smtplib

# model
from source.main.model.Users import Users
from source.main.model.GmailFrom import GmailFrom

sender = "admin@futurelove.online"
postmark_api = "c30887b4-230e-4c7a-9284-da22a2a373a4"
SECURITY_ALGORITHM = "HS256"
SECRET_KEY = "fbhe3hf839vbiwvc9wh30fbweocboeuwefiwehfwf9bvsfw9"

reusable_oauth2 = HTTPBearer(scheme_name="Authorization")


async def send_mail(email, link, user_name, device_register):
    try:
        body = f""" 
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">

            <head>
                <meta charset="UTF-8">
                <meta content="width=device-width, initial-scale=1" name="viewport">
                <meta name="x-apple-disable-message-reformatting">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta content="telephone=no" name="format-detection">
                <title></title>
                <!--[if (mso 16)]>
                <style type="text/css">
                
                </style>
                <![endif]-->
                
                <!--[if gte mso 9]>
            <xml>
                <o:OfficeDocumentSettings>
                <o:AllowPNG></o:AllowPNG>
                <o:PixelsPerInch>96</o:PixelsPerInch>
                </o:OfficeDocumentSettings>
            </xml>
            <![endif]-->
                <!--[if !mso]><!-- -->
                <link href="https://fonts.googleapis.com/css2?family=Imprima&display=swap" rel="stylesheet">
                <!--<![endif]-->
            </head>

            <body>
                <div dir="ltr" class="es-wrapper-color">
                    <!--[if gte mso 9]>
                        <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                            <v:fill type="tile" color="#ffffff"></v:fill>
                        </v:background>
                    <![endif]-->
                    <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                                <td class="esd-email-paddings" valign="top">
                                    <table cellpadding="0" cellspacing="0" class="es-footer esd-header-popover" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#bcb8b1" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" width="600">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p20t es-p20b es-p40r es-p40l" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-empty-container" style="display: none;"></td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-content" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" width="600" style="border-radius: 20px 20px 0 0 ">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p40t es-p40r es-p40l" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>

                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td class="es-p20t es-p40r es-p40l esd-structure" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%" bgcolor="#fafafa" style="background-color: #fafafa; border-radius: 10px; border-collapse: separate;">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="left" class="esd-block-text es-p20">
                                                                                                    <h3>Welcome, {user_name}</h3>
                                                                                                    <p><br></p>
                                                                                                    <p>You recently requested to open your Future Love account. Use the button below to confirmation.<br><br>Confirm your email address by clicking the button below. This step adds extra security to your business by verifying you own this email.</p>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-content" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" width="600">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p30t es-p40b es-p40r es-p40l" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-button">
                                                                                                    <!--[if mso]><a href="" target="_blank" hidden>
                <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" esdevVmlButton href="{link}" 
                            style="height:56px; v-text-anchor:middle; width:520px" arcsize="50%" stroke="f"  fillcolor="#fff">
                    <w:anchorlock></w:anchorlock>
                    <center style='color:#ffffff; font-family:Imprima, Arial, sans-serif; font-size:22px; font-weight:700; line-height:22px;  mso-text-raise:1px'>Confirm email</center>
                </v:roundrect></a>
            <![endif]-->
                                                                                                    <!--[if !mso]><!-- --><span class="msohide es-button-border" style="display: block; background: #fff;"><a href="{link}" class="es-button msohide" target="_blank" style="padding-left: 5px; padding-right: 5px; display: block; background: #fff; mso-border-alt: 10px solid  #fff">Confirm email</a></span>
                                                                                                    <!--<![endif]-->
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td class="esd-structure es-p40r es-p40l" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="left" class="esd-block-text">
                                                                                                    <p>Thanks,<br><br>Future Love Team!</p>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-spacer es-p40t es-p20b" style="font-size:0">
                                                                                                    <table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td style="border-bottom: 1px solid #666666; background: unset; height: 1px; width: 100%; margin: 0px;"></td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-content" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" width="600" style="border-radius: 0 0 20px 20px">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p20t es-p20b es-p40r es-p40l esdev-adapt-off" align="left">
                                                                    <table width="520" cellpadding="0" cellspacing="0" class="esdev-mso-table">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td class="esdev-mso-td" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" align="left" class="es-left">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td width="47" class="esd-container-frame" align="center" valign="top">
                                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="center" class="esd-block-image es-m-txt-l" style="font-size: 0px;"><a target="_blank" href="https://ibb.co/c3Tqtm0"><img src="https://i.ibb.co/h980Hqb/love.png" alt="Demo" style="display: block;" width="47" title="Demo"></a></td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                                <td width="20"></td>
                                                                                <td class="esdev-mso-td" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" class="es-right" align="right">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td width="453" class="esd-container-frame" align="center" valign="top">
                                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="left" class="esd-block-text">
                                                                                                                    <p style="font-size: 16px;">This link expire in 24 hours. If you have questions, <a target="_blank" style="font-size: 16px;" href="https://viewstripo.email">we're here to help</a></p>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-footer" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#bcb8b1" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" width="600">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p40t es-p30b es-p20r es-p20l" align="left" esd-custom-block-id="853188">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="560" align="left" class="esd-container-frame">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-image es-p20b es-m-txt-c" style="font-size: 0px;"><a target="_blank"><img src="https://i.ibb.co/h980Hqb/love.png" alt="Logo" style="display: block; font-size: 12px;" title="Logo" height="60"></a></td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-social es-m-txt-c es-p10t es-p20b" style="font-size:0">
                                                                                                    <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="center" valign="top" esd-tmp-icon-type="twitter" class="es-p5r"><a target="_blank" href><img src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/twitter-logo-black.png" alt="Tw" title="Twitter" height="24"></a></td>
                                                                                                                <td align="center" valign="top" esd-tmp-icon-type="facebook" class="es-p5r"><a target="_blank" href><img src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/facebook-logo-black.png" alt="Fb" title="Facebook" height="24"></a></td>
                                                                                                                <td align="center" valign="top" esd-tmp-icon-type="linkedin"><a target="_blank" href><img src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/linkedin-logo-black.png" alt="In" title="Linkedin" height="24"></a></td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-text" esd-links-underline="none">
                                                                                                    <p style="font-size: 13px;"><a target="_blank" style="text-decoration: none;"></a><a target="_blank" style="text-decoration: none;">Privacy Policy</a><a target="_blank" style="font-size: 13px; text-decoration: none;"></a> • <a target="_blank" style="text-decoration: none;">Unsubscribe</a></p>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-text es-p20t" esd-links-underline="none">
                                                                                                    <p><a target="_blank"></a>Copyright © 2023 ThinkDiff Company<a target="_blank"></a></p>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-footer esd-footer-popover" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center" esd-custom-block-id="819294">
                                                    <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" width="600">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p20" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="560" class="esd-container-frame" align="left">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-empty-container" style="display: none;"></td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </body>

            </html>
"""

        msg = MIMEText(body, "html")
        msg["To"] = email
        msg["From"] = sender
        msg["Subject"] = "FutureLove Account Register - Generate Images With AI"
        server = smtplib.SMTP("smtp.postmarkapp.com", 587)
        server.starttls()
        server.login(
            env.get("POSTMARK_API_KEY", "afed6e53-a372-4319-b08f-b8eba39c4b40"),
            env.get("POSTMARK_API_KEY", "afed6e53-a372-4319-b08f-b8eba39c4b40"),
        )
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the email:")
        print(str(e))
        return str(e)


async def send_mail_reset(email, password_new):

    postmark = PostmarkClient(server_token=postmark_api)
    postmark.emails.send(
        From=sender,
        To=email,
        Subject="FutureLove Account Register - Generate Images With AI",
        HtmlBody=f"Your new password is: {password_new}",
    )


async def send_mail_swap_done(id_user, link):
    try:
        account = db.session.query(Users.email).filter(Users.id_user == id_user).first()
        if account is not None:
            email = account[0]
            print(f"User email: {email}")
        else:
            print("No user found with the specified ID.")
        postmark = PostmarkClient(server_token=postmark_api)
        postmark.emails.send(
            From=sender,
            To=email,
            Subject="Generate Images And Video With AI",
            HtmlBody=f"Congratulations on using our company's Artificial Intelligence feature. From an input photo containing your face, we have generated a video containing your face. Here is the detailed link to watch that video: {link}, please experience and compare with the original video, thank you!",
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


async def send_mail_notifi(email, message):

    postmark = PostmarkClient(server_token=postmark_api)
    postmark.emails.send(
        From=sender,
        To=email,
        Subject="FutureLove Account Register - Generate Images With AI",
        HtmlBody=message,
    )


async def send_mail_del_account(email, message):

    postmark = PostmarkClient(server_token=postmark_api)
    postmark.emails.send(
        From=sender,
        To=email,
        Subject="FutureLove Account Register - Generate Images With AI",
        HtmlBody=message,
    )


def generate_token(username: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * 30  # Expired after 3 days
    )
    to_encode = {"exp": expire, "username": username}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


def verify_password(username, password):
    thong_tin = {}
    try:
        user = Users.query.filter(
            or_(Users.user_name == username, Users.email == username)
        )
        print("user_name___" + str(username) + "____email___" + str(password))
        print("____@@@@@@@____" + str(user) + "__count__" + str(len(user)) + "+++___")
        if len(user) == 0:
            return JSONResponse(
                content={"message": "Invalid Username Or Account Not Register!!"}
            )
        if user is not None:
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
                # thong_tin["cover_pic"] = user[0][10]
                return thong_tin
            return JSONResponse(content={"message": "Invalid Password!!"})
        else:
            return JSONResponse(
                content={"message": "Invalid Username Or Account Not Register!!"}
            )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


abc = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ1MDM0MzksInVzZXJuYW1lIjoiMjAwMjEzODhAdm51LmVkdS52biJ9.BoQtteOqGdTPhvapWQg3YZAAzzom1DPAQusVLsWcoTk"


def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(
            http_authorization_credentials.credentials,
            SECRET_KEY,
            algorithms=[SECURITY_ALGORITHM],
        )
        print(payload)
        expiration_time = payload.get("exp")
        current_time = datetime.now().timestamp()
        if expiration_time < current_time:
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get("username")
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )


async def save_user_to_mysql(
    user_name, password, email, link_avatar, ip_register, device_register, type_register
):
    try:
        max_id_user = db.session.query(func.max(Users.id_user)).scalar()
        id_user = max_id_user + 1
        count_sk = 0
        count_view = 0
        count_comment = 0
        save_user = Users(
            id_user=id_user,
            user_name=user_name,
            password=password,
            email=email,
            link_avatar=link_avatar,
            ip_register=ip_register,
            device_register=device_register,
            count_sukien=count_sk,
            count_comment=count_view,
            count_view=count_comment,
            type_register=type_register,
        )
        db.session.add(save_user)
        db.session.commit()
        return JSONResponse(
            content={"message": "The command was added successfully"}, status_code=200
        )
    except Exception as error:
        db.session.rollback()
        print(f"Failed to connect to MySQL database: {error}")
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# GET DATA GMAIL FROM USER AND GMAIL FROM
def get_data_email():
    try:
        gmail_data = db.session.query(GmailFrom.gmail, GmailFrom.password_app).all()
        # Choose a random row from gmail_data
        if gmail_data:
            data = random.choice(gmail_data)
            print("------gmail and password-----", str(data))
            return data
        else:
            print("No records found.")
            return None
    except Exception as error:
        print(f"Error Exception: {error}")
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


def get_user_email(id_user):
    try:
        data = db.session.query(Users.email).filter(Users.id_user == id_user).filter()
        if data:
            print("------user-----", str(data))
            return data
        else:
            print("No records found.")
            return None
    except Exception as error:
        print(f"Error Exception: {error}")
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# send email by email
# async def send_email_MakeWedding(gmail_from: str, gmail_app_password: str, gmail_to: str, link: str, link_video:str):


async def send_email_MakeWedding(
    gmail_from: str, gmail_app_password: str, gmail_to: str, link: str
):
    sent_subject = "Congratulations on Successfully Creating Wedding Photos Using AI"
    sent_body = f"It's amazing, we used AI algorithms to create wedding photos of you and your spouse. We will send a web link to your wedding photos. Please save your wedding photos. If this web link is generated for free, it will only be stored for a short time on the server. You can share this image web link with your friends.  Thank you \n That tuyet voi, He thong tri tue nhan tao da sinh ra link tong hop anh? do he thong AI Sinh ra, hay trai nghiem  no : {link}"
    # sent_body = f"It's amazing, we used AI algorithms to create wedding photos of you and your spouse. We will send a web link to your wedding photos. Please save your wedding photos. If this web link is generated for free, it will only be stored for a short time on the server. You can share this image web link with your friends.  Thank you \n That tuyet voi, He thong tri tue nhan tao da sinh ra link tong hop anh? do he thong AI Sinh ra, hay trai nghiem  no : {link}\n Day la video tao duoc tu hinh anh cua ban : {link_video}"
    msg = EmailMessage()
    msg["Subject"] = sent_subject
    msg["From"] = gmail_from
    msg["To"] = gmail_to
    msg.set_content(
        f"""\
            {sent_body}
        """
    )
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_from, gmail_app_password)
        server.send_message(msg)
        server.close()
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
    return "Send email success!!!"


async def send_email_MakeWedding_video(
    gmail_from: str, gmail_app_password: str, gmail_to: str, link: str
):
    sent_subject = "Congratulations on Successfully Creating Video Wedding"
    sent_body = f"You can watch your video here : {link}"

    msg = EmailMessage()
    msg["Subject"] = sent_subject
    msg["From"] = gmail_from
    msg["To"] = gmail_to
    msg.set_content(
        f"""\
            {sent_body}
        """
    )
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_from, gmail_app_password)
        server.send_message(msg)
        server.close()
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
    return "Send email success!!!"


async def send_email_to_swap_done(
    gmail_from: str, gmail_app_password: str, gmail_to: str, link: str
):
    sent_subject = "FutureLove Notification - Generate Images With AI"
    sent_body = f"Congratulations on using our company's Artificial Intelligence feature. From an input photo containing your face, we have generated a video containing your face. Here is the detailed link to watch that video: {link}, please experience and compare with the original video, thank you!"
    msg = EmailMessage()
    msg["Subject"] = sent_subject
    msg["From"] = gmail_from
    msg["To"] = gmail_to
    msg.set_content(
        f"""\
            {sent_body}
        """
    )
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_from, gmail_app_password)
        server.send_message(msg)
        server.close()
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
    return "Send email success!!!"


# SEND EMAIL WHEN SWAP DONE
# async def get_id_user_send_fakewedding_email(id_user, link, link_video):
async def get_id_user_send_fakewedding_email(id_user, link):
    try:
        data = get_data_email()
        # Execute the SQL query to retrieve data from user table
        data2 = get_user_email(id_user)
        print(data2)
        await send_email_MakeWedding(data[0], data[1], data2[0], link)
        # await send_email_MakeWedding(data[0], data[1], data2[0], link, link_video)
    except Exception as error:
        print(f"Error Exception: {error}")
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


async def get_id_user_send_fakewedding_email_video(id_user, link):
    try:
        data = get_data_email()

        # Execute the SQL query to retrieve data from user table
        data2 = get_user_email(id_user)
        print(data2)
        await send_email_MakeWedding_video(data[0], data[1], data2[0], link)
        # await send_email_MakeWedding(data[0], data[1], data2[0], link, link_video)
    except Exception as error:
        print(f"Error Exception: {error}")
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


async def get_id_user_receved_email(id_user, link):
    try:
        data = get_data_email()

        # Execute the SQL query to retrieve data from user table
        data2 = get_user_email(id_user)
        print(data2)
        await send_email_to_swap_done(data[0], data[1], data2[0], link)
    except Exception as error:
        print(f"Error Exception: {error}")
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


# SEND EMAIL TO RESET LOGIN
async def send_mail_to_email_reset(email, password_new):
    try:
        data = get_data_email()
        Subject = "FutureLove Account Register - Generate Images With AI"
        HtmlBody = f"Your new password is: {password_new}"
        msg = EmailMessage()
        msg["Subject"] = Subject
        msg["From"] = data[0]
        msg["To"] = email
        msg.set_content(
            f"""\
                {HtmlBody}
            """
        )
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login(data[0], data[1])
            server.send_message(msg)
            server.close()
        except Exception as exception:
            print("Error: %s!\n\n" % exception)
        return "Send email success!!!"
    except Exception as error:
        print(f"Error Exception: {error}")
        raise HTTPException(status_code=500, detail=f"Error Exception: {error}")


async def send_email_to_notifi(gmail_to: str, message: str):
    data = get_data_email()
    sent_subject = "FutureLove Notification - Generate Images With AI"
    sent_body = message
    msg = EmailMessage()
    msg["Subject"] = sent_subject
    msg["From"] = data[0]
    msg["To"] = gmail_to
    msg.set_content(
        f"""\
            {sent_body}
        """
    )
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(data[0], data[1])
        server.send_message(msg)
        server.close()
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
    return "Send email success!!!"


async def send_email_to_del_account(gmail_to: str, message: str):
    data = get_data_email()
    sent_subject = ("FutureLove Account Register - Generate Images With AI",)
    sent_body = message
    msg = EmailMessage()
    msg["Subject"] = sent_subject
    msg["From"] = data[0]
    msg["To"] = gmail_to
    msg.set_content(
        f"""\
            {sent_body}
        """
    )
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(data[0], data[1])
        server.send_message(msg)
        server.close()
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
    return "Send email success!!!"


async def send_mail_to_email(email, link, user_name, device_register):
    try:

        MainData_body = f""" 
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">

            <head>
                <meta charset="UTF-8">
                <meta content="width=device-width, initial-scale=1" name="viewport">
                <meta name="x-apple-disable-message-reformatting">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta content="telephone=no" name="format-detection">
                <title></title>
                <!--[if (mso 16)]>
                <style type="text/css">
                
                </style>
                <![endif]-->
                
                <!--[if gte mso 9]>
            <xml>
                <o:OfficeDocumentSettings>
                <o:AllowPNG></o:AllowPNG>
                <o:PixelsPerInch>96</o:PixelsPerInch>
                </o:OfficeDocumentSettings>
            </xml>
            <![endif]-->
                <!--[if !mso]><!-- -->
                <link href="https://fonts.googleapis.com/css2?family=Imprima&display=swap" rel="stylesheet">
                <!--<![endif]-->
            </head>

            <body>
                <div dir="ltr" class="es-wrapper-color">
                    <!--[if gte mso 9]>
                        <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                            <v:fill type="tile" color="#ffffff"></v:fill>
                        </v:background>
                    <![endif]-->
                    <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0">
                        <tbody>
                            <tr>
                                <td class="esd-email-paddings" valign="top">
                                    <table cellpadding="0" cellspacing="0" class="es-footer esd-header-popover" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#bcb8b1" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" width="600">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p20t es-p20b es-p40r es-p40l" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-empty-container" style="display: none;"></td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-content" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" width="600" style="border-radius: 20px 20px 0 0 ">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p40t es-p40r es-p40l" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>

                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td class="es-p20t es-p40r es-p40l esd-structure" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%" bgcolor="#fafafa" style="background-color: #fafafa; border-radius: 10px; border-collapse: separate;">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="left" class="esd-block-text es-p20">
                                                                                                    <h3>Welcome, {user_name}</h3>
                                                                                                    <p><br></p>
                                                                                                    <p>You recently requested to open your Future Love account. Use the button below to confirmation.<br><br>Confirm your email address by clicking the button below. This step adds extra security to your business by verifying you own this email.</p>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-content" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" width="600">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p30t es-p40b es-p40r es-p40l" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-button">
                                                                                                    <!--[if mso]><a href="" target="_blank" hidden>
                <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" esdevVmlButton href="{link}" 
                            style="height:56px; v-text-anchor:middle; width:520px" arcsize="50%" stroke="f"  fillcolor="#fff">
                    <w:anchorlock></w:anchorlock>
                    <center style='color:#ffffff; font-family:Imprima, Arial, sans-serif; font-size:22px; font-weight:700; line-height:22px;  mso-text-raise:1px'>Confirm email</center>
                </v:roundrect></a>
            <![endif]-->
                                                                                                    <!--[if !mso]><!-- --><span class="msohide es-button-border" style="display: block; background: #fff;"><a href="{link}" class="es-button msohide" target="_blank" style="padding-left: 5px; padding-right: 5px; display: block; background: #fff; mso-border-alt: 10px solid  #fff">Confirm email</a></span>
                                                                                                    <!--<![endif]-->
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td class="esd-structure es-p40r es-p40l" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="520" class="esd-container-frame" align="center" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="left" class="esd-block-text">
                                                                                                    <p>Thanks,<br><br>Future Love Team!</p>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-spacer es-p40t es-p20b" style="font-size:0">
                                                                                                    <table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td style="border-bottom: 1px solid #666666; background: unset; height: 1px; width: 100%; margin: 0px;"></td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-content" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" width="600" style="border-radius: 0 0 20px 20px">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p20t es-p20b es-p40r es-p40l esdev-adapt-off" align="left">
                                                                    <table width="520" cellpadding="0" cellspacing="0" class="esdev-mso-table">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td class="esdev-mso-td" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" align="left" class="es-left">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td width="47" class="esd-container-frame" align="center" valign="top">
                                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="center" class="esd-block-image es-m-txt-l" style="font-size: 0px;"><a target="_blank" href="https://ibb.co/c3Tqtm0"><img src="https://i.ibb.co/h980Hqb/love.png" alt="Demo" style="display: block;" width="47" title="Demo"></a></td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                                <td width="20"></td>
                                                                                <td class="esdev-mso-td" valign="top">
                                                                                    <table cellpadding="0" cellspacing="0" class="es-right" align="right">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td width="453" class="esd-container-frame" align="center" valign="top">
                                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="left" class="esd-block-text">
                                                                                                                    <p style="font-size: 16px;">This link expire in 24 hours. If you have questions, <a target="_blank" style="font-size: 16px;" href="https://viewstripo.email">we're here to help</a></p>
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-footer" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center">
                                                    <table bgcolor="#bcb8b1" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" width="600">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p40t es-p30b es-p20r es-p20l" align="left" esd-custom-block-id="853188">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="560" align="left" class="esd-container-frame">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-image es-p20b es-m-txt-c" style="font-size: 0px;"><a target="_blank"><img src="https://i.ibb.co/h980Hqb/love.png" alt="Logo" style="display: block; font-size: 12px;" title="Logo" height="60"></a></td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-social es-m-txt-c es-p10t es-p20b" style="font-size:0">
                                                                                                    <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social">
                                                                                                        <tbody>
                                                                                                            <tr>
                                                                                                                <td align="center" valign="top" esd-tmp-icon-type="twitter" class="es-p5r"><a target="_blank" href><img src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/twitter-logo-black.png" alt="Tw" title="Twitter" height="24"></a></td>
                                                                                                                <td align="center" valign="top" esd-tmp-icon-type="facebook" class="es-p5r"><a target="_blank" href><img src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/facebook-logo-black.png" alt="Fb" title="Facebook" height="24"></a></td>
                                                                                                                <td align="center" valign="top" esd-tmp-icon-type="linkedin"><a target="_blank" href><img src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/linkedin-logo-black.png" alt="In" title="Linkedin" height="24"></a></td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-text" esd-links-underline="none">
                                                                                                    <p style="font-size: 13px;"><a target="_blank" style="text-decoration: none;"></a><a target="_blank" style="text-decoration: none;">Privacy Policy</a><a target="_blank" style="font-size: 13px; text-decoration: none;"></a> • <a target="_blank" style="text-decoration: none;">Unsubscribe</a></p>
                                                                                                </td>
                                                                                            </tr>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-block-text es-p20t" esd-links-underline="none">
                                                                                                    <p><a target="_blank"></a>Copyright © 2023 ThinkDiff Company<a target="_blank"></a></p>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table cellpadding="0" cellspacing="0" class="es-footer esd-footer-popover" align="center">
                                        <tbody>
                                            <tr>
                                                <td class="esd-stripe" align="center" esd-custom-block-id="819294">
                                                    <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0" width="600">
                                                        <tbody>
                                                            <tr>
                                                                <td class="esd-structure es-p20" align="left">
                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td width="560" class="esd-container-frame" align="left">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td align="center" class="esd-empty-container" style="display: none;"></td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </body>

            </html>
"""
        print("_____truoc_khi_guimail_____")
        data = get_data_email()
        print("_________" + data[0], [data[1]])
        # msg = MIMEText(body, "html")
        # msg["To"] = email
        # msg["From"] = data[0]
        # msg["Subject"] = "FutureLove Account Register - Generate Images With AI"
        # server = smtplib.SMTP("smtp.postmarkapp.com", 587)
        # print("_____SONPRO_____")
        # print(data[0])
        # print(data[1])
        # server.starttls()
        # server.login(data[0], data[1])
        # server.sendmail(msg["From"], msg["To"], msg.as_string())
        # server.quit()
        # print("Email sent successfully!")
        msg = EmailMessage()
        msg["Subject"] = "Verify Account AI Make Wedding Online"
        msg["From"] = "devmobilepro1888@gmail.com"
        msg["To"] = email
        msg.set_content(
            f"""\
            {MainData_body}
        """,
            subtype="html",
        )
        print("_________________________________________________")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(data[0], data[1])
        server.send_message(msg)

        server.close()
    except Exception as e:
        print("An error occurred while sending the email:")
        print(str(e))
        print(email, link, user_name, device_register)
        return str(e)
