import csv
import random
import time
import os
from PIL import Image
from gensk import skgendata, skgendatangam, skgendatanoel
from datetime import datetime
import asyncio
import uuid
import cairosvg
from PIL import Image
import io
from source import db
from source.main.model.SavedSuKien import SavedSuKien
from source.main.model.SavedSuKienAlone import SavedSuKienAlone
from source.main.model.SavedSuKien2Img import SavedSuKien2Img
from source.main.model.SavedSuKienSwapBaby import SavedSuKienSwapBaby
from source.main.model.SavedSuKienVideo import SavedSuKienVideo
from source.main.model.SavedSKVideoSwapImage import SavedSKVideoSwapImage
from source.main.model.SavedSKVideoImageGrowup import SavedSKVideoImageGrowup
from source.main.model.SavedSKVideoImageMeBau import SavedSKVideoImageMeBau
from source.main.model.WeddingDetail import WeddingDetail
from source.main.model.AloneTemplate import AloneTemplate
from source.main.model.ListImageAlone import ListImageAlone
from source.main.model.SavedSKVideoImageWedding import SavedSKVideoImageWedding

def get_random_data():
    result_data = []
    list_sk = skgendata()
    print(list_sk)
    seed = int(time.time())

    # Thiết lập seed cho hàm random
    random.seed(seed)
    i = 0

    folder = "/var/www/build_futurelove/image/image_sk"

    for sk_filename in list_sk:
        csv_file_path = f"./sukien/{sk_filename}.csv"
        random_ids = random.sample(range(1, 25), 1)
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                # print("ROW___" + str(row))
                # print("random_ids___" + str(random_ids))
                id = int(row["id"]) in random_ids
                if id != 0:
                    folder_path_nam = (
                        f'{folder}/{sk_filename}/{sk_filename}_nam/{row["id"]}.jpg'
                    )
                    folder_path_nu = (
                        f'{folder}/{sk_filename}/{sk_filename}_nu/{row["id"]}.jpg'
                    )
                    data = {
                        "id": row["id"],
                        "id_num": i + 1,
                        "tensukien": sk_filename,
                        "thongtin": row["thongtin"],
                        "image": row["image"],
                        "nu": folder_path_nu,
                        "nam": folder_path_nam,
                        "vtrinam": row["vtrinam"],
                        "tomLuocText": row["tomLuocText"],
                    }
                    i = i + 1
                    result_data.append(data)

    return result_data


def get_random_data_swap_baby():
    result_data = []
    seed = int(time.time())
    # Thiết lập seed cho hàm random
    random.seed(seed)
    csv_file_path = f"./sukien/file1.csv"
    random_ids = random.sample(range(1, 100), 1)
    with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if int(row["id"]) == random_ids[0]:
                data = {
                    "id": row["id"],
                    "thongtin": row["thongtin"],
                    "tomLuocText": row["tomLuocText"],
                }
                result_data.append(data)
                break
    return result_data


def get_random_data_check(sk_filename):
    result_data = []
    seed = int(time.time())

    # Thiết lập seed cho hàm random
    random.seed(seed)
    i = 0

    csv_file_path = f"./sukien/{sk_filename}.csv"

    with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            if int(row["id"]) in range(1, 26):
                data = {
                    "id": row["id"],
                    "id_num": i + 1,
                    "tensukien": sk_filename,
                    "thongtin": row["thongtin"],
                    "image": row["image"],
                    "nu": row["nu"],
                    "nam": row["nam"],
                    "vtrinam": row["vtrinam"],
                    "tomLuocText": row["tomLuocText"],
                }
                i = i + 1
                result_data.append(data)

    return result_data


def get_random_data_skngam():
    result_data = []
    list_sk = skgendatangam()
    print(list_sk)
    seed = int(time.time())

    # Thiết lập seed cho hàm random
    random.seed(seed)
    i = 0
    folder = "/var/www/build_futurelove/image/image_sk"
    for sk_filename in list_sk:
        csv_file_path = f"./sukien/{sk_filename}.csv"
        random_ids = random.sample(range(1, 25), 1)
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                if int(row["id"]) in random_ids:
                    folder_path_nam = (
                        f'{folder}/{sk_filename}/{sk_filename}_nam/{row["id"]}.jpg'
                    )
                    folder_path_nu = (
                        f'{folder}/{sk_filename}/{sk_filename}_nu/{row["id"]}.jpg'
                    )
                    data = {
                        "id": row["id"],
                        "id_num": i + 1,
                        "tensukien": sk_filename,
                        "thongtin": row["thongtin"],
                        "image": row["image"],
                        "nu": folder_path_nu,
                        "nam": folder_path_nam,
                        "vtrinam": row["vtrinam"],
                        "tomLuocText": row["tomLuocText"],
                    }
                    i = i + 1
                    result_data.append(data)

    return result_data


def merge_image(list_data, folder_path):
    print(list_data)
    # Tạo một dictionary để lưu trữ các ảnh theo chỉ số "i"
    image_dict = {}
    print("folder", folder_path)
    # Lặp qua tất cả các tệp trong thư mục
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            parts = filename.split("_")
            if len(parts) == 2:
                key = parts[1].split(".")[0]  # Lấy chỉ số "i" từ tên file
                if key not in image_dict:
                    image_dict[key] = []
                image_dict[key].append(filename)

    combined_dict = {}
    sorted_dict = {}
    for key, values in image_dict.items():
        nam_values = []
        nu_values = []
        for value in values:
            if value.startswith("nam_"):
                nam_values.append(value)
            elif value.startswith("nu_"):
                nu_values.append(value)
        sorted_dict[key] = nam_values + nu_values

    combined_dict = sorted_dict.copy()  # Sao chép dict ban đầu để tạo dict mới
    print("imagedict: ", image_dict)
    for item in list_data:
        id_value = str(item["id"])  # Chuyển id từ int sang str để so sánh
        vtrinam_value = item["vtrinam"]

        if id_value in combined_dict:
            combined_dict[id_value].append(vtrinam_value)
    print(combined_dict)
    # Lặp qua các cặp ảnh cùng chỉ số "i" và ghép chúng lại
    for key, filenames in combined_dict.items():
        if len(filenames) == 3:
            if filenames[2] == "1":
                filenames.remove("1")
                images = [
                    Image.open(os.path.join(folder_path, filename))
                    for filename in filenames
                ]
                widths, heights = zip(*(i.size for i in images))
                total_width = sum(widths)
                max_height = max(heights)
                new_im = Image.new("RGB", (total_width, max_height))
                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset, 0))
                    x_offset += im.size[0]
                new_im.save(os.path.join(folder_path, f"AI_gen_{key}.jpg"))
                for filename in filenames:
                    os.remove(os.path.join(folder_path, filename))

            elif filenames[2] == "0":
                filenames.remove("0")
                images = [
                    Image.open(os.path.join(folder_path, filename))
                    for filename in filenames
                ]
                images.reverse()
                widths, heights = zip(*(i.size for i in images))
                total_width = sum(widths)
                max_height = max(heights)
                new_im = Image.new("RGB", (total_width, max_height))
                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset, 0))
                    x_offset += im.size[0]
                new_im.save(os.path.join(folder_path, f"AI_gen_{key}.jpg"))

                for filename in filenames:
                    os.remove(os.path.join(folder_path, filename))

    print("Hoàn thành việc ghép ảnh.")


def insert_svg_logo(image_folder):
    logo_path = "./logo.svg"
    # Đọc nội dung của file SVG
    with open(logo_path, "r") as f:
        svg_content = f.read()

    text_path = "./text.png"

    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path)

            # Chuyển đổi SVG sang PNG
            svg_data = cairosvg.svg2png(bytestring=svg_content)
            logo = Image.open(io.BytesIO(svg_data))

            text = Image.open(text_path)

            text_width, text_height = text.size
            new_text_width = int(image.width * 0.2)
            new_text_height = int(text_height * (new_text_width / text_width))
            resized_text = text.resize((new_text_width, new_text_height))
            # Tính toán kích thước mới cho logo
            logo_width, logo_height = logo.size
            new_logo_width = int(image.width * 0.1)
            new_logo_height = int(logo_height * (new_logo_width / logo_width))
            resized_logo = logo.resize((new_logo_width, new_logo_height))

            # Thay thế nền trắng của logo bằng độ trong suốt
            resized_logo = resized_logo.convert("RGBA")
            logo_data = resized_logo.getdata()
            new_logo_data = []
            for item in logo_data:
                # Thay thế màu trắng (255, 255, 255) thành (255, 255, 255, 0)
                if item[:3] == (255, 255, 255):
                    new_logo_data.append((255, 255, 255, 0))
                else:
                    new_logo_data.append(item)
            resized_logo.putdata(new_logo_data)

            # Tính toán vị trí để chèn logo vào ảnh
            offset = (
                image.width - resized_logo.width - 10,
                image.height - resized_logo.height - 10,
            )

            offset_bottom_center = (
                (image.width - resized_text.width) // 2,
                image.height - resized_text.height - 5,
            )  # Vị trí trung tâm dưới cùng

            # Chèn logo vào ảnh
            image.paste(resized_logo, offset, resized_logo)

            image_with_logo_bottom_center = image.copy()
            image_with_logo_bottom_center.paste(
                resized_text, offset_bottom_center, resized_text
            )

            # Tạo đường dẫn đến thư mục xuất ra
            output_path = os.path.join(image_folder, filename)

            # Lưu ảnh đã chèn logo
            image_with_logo_bottom_center.save(output_path)

    print("Hoàn thành chèn logo vào ảnh!")


def save_to_mysql(data, link1, link2, device_them_su_kien, ip_them_su_kien, id_user_ne, ten_nam, ten_nu):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    
    try:
        for items in data:
            items["numswap"] = items["vtrinam"]
            items["id_toan_bo_su_kien"] = id_toan_bo_sk
            date = datetime.now()
            id_template = random.randint(1, 4)
            
            # Create a new event record
            new_sukien = SavedSuKien(
                id_saved=id_toan_bo_sk,
                link_nam_goc=link1,
                link_nu_goc=link2,
                link_nam_chua_swap=items["nam"],
                link_nu_chua_swap=items["nu"],
                link_da_swap=items["link_img"],
                thoigian_swap=date,
                ten_su_kien=items["tensukien"],
                noidung_su_kien=items["thongtin"],
                id_toan_bo_su_kien=id_toan_bo_sk,
                so_thu_tu_su_kien=items['id_num'],
                thoigian_sukien=date,
                device_them_su_kien=device_them_su_kien,
                ip_them_su_kien=ip_them_su_kien,
                id_user=id_user_ne,
                tomLuocText=items["tomLuocText"],
                ten_nam=ten_nam,
                ten_nu=ten_nu,
                count_comment=count_comment,
                count_view=count_view,
                id_template=id_template,
                phantram_loading=items['id_num'] * 10
            )
            
            # Add to the session
            db.session.add(new_sukien)
        db.session.commit()
        
        print("Data inserted successfully")
        return data
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error inserting data: {e}")
    
    finally:
        db.session.close()  



def save_to_mysql_skngam(
    data,
    link1,
    link2,
    id_toan_bo_su_kien,
    device_them_su_kien,
    ip_them_su_kien,
    id_user_ne,
    ten_nam,
    ten_nu,
):
    count_comment = 0
    count_view = 0
    try:
        for items in data:
            items["numswap"] = items["vtrinam"]
            items["id_toan_bo_su_kien"] = id_toan_bo_su_kien
            date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            id_template = random.randint(1, 4)
            new_skngam = SavedSuKien(
                id_saved=id_toan_bo_su_kien,
                link_nam_goc=link1,
                link_nu_goc=link2,
                link_nam_chua_swap=items["nam"],
                link_nu_chua_swap=items["nu"],
                link_da_swap=items["link_img"],
                thoigian_swap=date,
                ten_su_kien=items["tensukien"],
                noidung_su_kien=items["thongtin"],
                id_toan_bo_su_kien=id_toan_bo_su_kien,
                so_thu_tu_su_kien=items['id_num'],
                thoigian_sukien=date,
                device_them_su_kien=device_them_su_kien,
                ip_them_su_kien=ip_them_su_kien,
                id_user=id_user_ne,
                tomLuocText=items["tomLuocText"],
                ten_nam=ten_nam,
                ten_nu=ten_nu,
                count_comment=count_comment,
                count_view=count_view,
                id_template=id_template,
                phantram_loading=(items['id_num'] + 6) * 10
            )
            # Add to the session
            db.session.add(new_skngam)
        # commit to the session
        db.session.commit()
        print("Data inserted successfully")
        return data
    except Exception as e:
        db.session.rollback()
        print(f"Error inserting data: {e}")
    finally:
        db.session.close()


def save_to_mysql_anh_don(link,link_swap,device_them_su_kien,ip_them_su_kien,id_user,loai_sukien,album,id_sk_album):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0

    try:
        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        id_template = random.randint(1, 4)
        print(loai_sukien)
        Json_added = {
                "id_saved": id_toan_bo_sk,
                "link_src_goc": link,
                "link_da_swap": link_swap,
                "id_toan_bo_su_kien": id_toan_bo_sk,
                "thoigian_sukien": date,
                "device_them_su_kien": device_them_su_kien,
                "ip_them_su_kien": ip_them_su_kien,
                "id_user": id_user,
                "count_comment": count_comment,
                "count_view": count_view,
                "id_template": id_template,
                "loai_sukien": loai_sukien,
                "id_all_sk": id_sk_album,
        }
        new_sk_alone = SavedSuKienAlone(
                id_saved = id_toan_bo_sk,
                link_src_goc = link,
                link_da_swap = link_swap,
                id_toan_bo_su_kien = id_toan_bo_sk,
                thoigian_sukien  = date,
                device_them_su_kien = device_them_su_kien,
                ip_them_su_kien = ip_them_su_kien,
                id_user = id_user,
                count_comment = count_comment,
                count_view = count_view,
                id_template  = id_template,
                loai_sukien = loai_sukien,
                album  = album,
                id_sk_album = id_sk_album,
        )
        db.session.add(new_sk_alone)
        db.session.commit()
        return Json_added
    except Exception as e:
        db.session.rollback()
        print(f"Error inserting data: {e}")
    finally:
        db.session.close()


def save_to_mysql_2_image(link1,link2,link_swap,device_them_su_kien,ip_them_su_kien,id_user,loai_sukien,album,id_sk_album):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    try:
        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        id_template = random.randint(1, 4)
        print(loai_sukien)
        Json_added = {
                "id_saved": id_toan_bo_sk,
                "link_src_goc": link1,
                "link_tar_goc": link2,
                "link_da_swap": link_swap,
                "id_toan_bo_su_kien": id_toan_bo_sk,
                "thoigian_sukien": date,
                "device_them_su_kien": device_them_su_kien,
                "ip_them_su_kien": ip_them_su_kien,
                "id_user": id_user,
                "count_comment": count_comment,
                "count_view": count_view,
                "id_template": id_template,
                "loai_sukien": loai_sukien,
                "id_all_sk": id_sk_album,
        }
        new_sk2_img = SavedSuKien2Img(
            id_saved  = id_toan_bo_sk,
            link_src_goc = link1,
            link_tar_goc = link2,
            link_da_swap = link_swap,
            id_toan_bo_su_kien = id_toan_bo_sk,
            thoigian_sukien = date,
            device_them_su_kien = device_them_su_kien,
            ip_them_su_kien = ip_them_su_kien,
            id_user = id_user,
            count_comment = count_comment,
            count_view = count_view,
            id_template = id_template,
            loai_sukien = loai_sukien,
            album = album,
            id_sk_album = id_sk_album
        )
        db.session.add(new_sk2_img)
        db.session.commit()
        return Json_added
    except Exception as error:
        db.session.rollback()
        print(f"Error inserting data: {error}")
        Json_added = {
            "id_saved": id_toan_bo_sk,
            "link_src_goc": link1,
            "link_tar_goc": link2,
            "link_da_swap": link_swap,
            "id_toan_bo_su_kien": id_toan_bo_sk,
            "thoigian_sukien": date,
            "device_them_su_kien": device_them_su_kien,
            "ip_them_su_kien": ip_them_su_kien,
            "id_user": id_user,
            "count_comment": count_comment,
            "count_view": count_view,
            "id_template": id_template,
            "loai_sukien": loai_sukien,
            "id_all_sk": id_sk_album,
            "message": "________________________________LOI EXPTION PHan MYSQL_______"
            + str(error),
        }
        print(f"Error inserting data: {error}")
        return Json_added


def save_to_mysql_swap_baby(data, device_them_su_kien, ip_them_su_kien, id_user):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0

    try:
        for items in data:
            items["id_toan_bo_su_kien"] = id_toan_bo_sk
            date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            id_template = random.randint(1, 4)
            new_swap_baby = SavedSuKienSwapBaby(
                id_saved = id_toan_bo_sk,
                link_nam_goc = items["link_nam_goc"],
                link_nu_goc = items["link_nu_goc"],
                link_baby_goc = items["link_baby_goc"],
                link_da_swap = items["link_da_swap"],
                id_toan_bo_su_kien = id_toan_bo_sk,
                noi_dung_su_kien = items["thongtin"],
                thoigian_sukien = date,
                device_them_su_kien = device_them_su_kien,
                ip_them_su_kien = ip_them_su_kien,
                id_user = id_user,
                tomLuocText = items["tomLuocText"],
                count_comment = count_comment,
                count_view = count_view,
                id_template = id_template,
            )
            # add
            db.session.add(new_swap_baby)
        # commit
        db.session.commit()
        return data
    except Exception as error:
        db.session.rollback()
        print(f"Error inserting data: {error}")
        return data


def save_video_to_mysql(
    link_vid_swap, thogian_swap, id_user, id_video, linkimg, ten_video, device, ip
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    base_url = "https://photo.gachmen.org"
    link_vid_goc = f"https://photo.gachmen.org/image/video_sk/{id_video}.mp4"
    linkimg = linkimg.replace("/var/www/build_futurelove", base_url)
    data = {}
    try:
        noidung = "abc"

        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data = {
                "id_sukien_video": id_toan_bo_sk,
                "id_video_swap": id_video,
                "linkimg": linkimg,
                "link_vid_swap": link_vid_swap,
                "link_vid_goc": link_vid_goc,
                "ten_video": ten_video,
                "noidung": noidung,
                "thoigian_sukien": date,
                "thoigian_swap": thogian_swap,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
        }
        new_video = SavedSuKienVideo(
            id_saved = id_toan_bo_sk,
            link_video = id_video,
            link_image = linkimg,
            link_da_swap = link_vid_swap,
            ten_su_kien = ten_video,
            noidung_su_kien = noidung,
            id_video = id_video,
            thoigian_sukien = date,
            device_them_su_kien = device,
            ip_them_su_kien = ip,
            id_user = id_user,
            count_comment = count_comment,
            count_view = count_view,
            link_video_goc = link_vid_goc,
            thoigian_swap = thogian_swap,
        )
        # add
        db.session.add(new_video)
        # commit
        db.session.commit()
        return data
    except Exception as error:
        db.session.rollback()
        print(
            f"_____________________________MySQL database: {error} ___________________-"
        )
        return data


def save_video_to_mysql_swap_imagevideo(
    src_image, src_video, link_vid_swap, id_user, device, ip
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    data = {}
    try:

        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data = {
                "id_saved": id_toan_bo_sk,
                "link_video_goc": src_video,
                "link_image": src_image,
                "link_vid_da_swap": link_vid_swap,
                "thoigian_sukien": date,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
        }
        new_sk_swap = SavedSKVideoSwapImage(
            id_saved = id_toan_bo_sk,
            link_video_goc = src_video,
            link_image = src_image,
            link_video_da_swap = link_vid_swap,
            thoigian_sukien = date,
            device_them_su_kien = device,
            ip_them_su_kien = ip,
            id_user = id_user,
            count_comment = count_comment,
            count_view = count_view,
        )
        # add
        db.session.add(new_sk_swap)
        # commit
        db.session.commit()
        return data
        
    except Exception as error:
        db.session.rollback()
        print(f"Error inserting data: {error}")
    finally:
       db.session.close()


def save_video_to_mysql_swap_imagevideo_growup(
    src_image, src_video, link_vid_swap, id_user, device, ip, loai_sk
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    data = {}
    try:
        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data = {
                "id_saved": id_toan_bo_sk,
                "link_video_goc": src_video,
                "link_image": src_image,
                "link_vid_da_swap": link_vid_swap,
                "thoigian_sukien": date,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": loai_sk,
        }
        new_sk_growup = SavedSKVideoImageGrowup(
            id_saved = id_toan_bo_sk,
            link_video_goc = src_video,
            link_image = src_image,
            link_video_da_swap = link_vid_swap,
            thoigian_sukien = date,
            device_them_su_kien = device,
            ip_them_su_kien = ip,
            loai_sk = loai_sk,
            id_user = id_user,
            count_comment = count_comment,
            count_view = count_view,
        )
        # add
        db.session.add(new_sk_growup)
        # commit
        db.session.commit()
        return data
    except Exception as error:
        db.session.rollback()
        print(
            f"_____Loi exception ____ save_video_to_mysql_swap_imagevideo_growup_____ {error}"
        )
        data = {
            "id_saved": id_toan_bo_sk,
            "link_video_goc": src_video,
            "link_image": src_image,
            "link_vid_da_swap": link_vid_swap,
            "thoigian_sukien": date,
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "Error": "-----loi swap anh------"
        }
        return data


# SAVE IMAGE VIDEO WEDDING SERVER


def save_video_to_mysql_swap_imagevideo_wedding(
    src_image, src_video, link_vid_swap, id_user, device, ip
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    data = {}
    try:
        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data = {
                "id_saved": id_toan_bo_sk,
                "link_video_goc": src_video,
                "link_image": src_image,
                "link_vid_da_swap": link_vid_swap,
                "thoigian_sukien": date,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
        }
        new_img_wedding = SavedSKVideoImageWedding(
            id_saved = id_toan_bo_sk,
            link_video_goc = src_video,
            link_image = src_image,
            link_video_da_swap = link_vid_swap,
            thoigian_sukien = date,
            device_them_su_kien = device,
            ip_them_su_kien = ip,
            id_user = id_user,
            count_comment = count_comment,
            count_view = count_view,
        )
        # add
        db.session.add(new_img_wedding)
        # commit
        db.session.commit()
        return data
    except Exception as error:
        db.session.rollback()
        print(f"_____Loi exception ____ SavedSKVideoImageWedding: {error}")
        data = {
            "id_saved": id_toan_bo_sk,
            "link_video_goc": src_video,
            "link_image": src_image,
            "link_vid_da_swap": link_vid_swap,
            "thoigian_sukien": date,
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
            "Error": "Luu su kien loi"
        }
        return data
    finally:
        db.session.close()

def get_images_alone(list_folder):
    try:
        alone_template = AloneTemplate.query.filter_by(folder_name = list_folder).first()

        if alone_template is None:
            print("No folder with name '{folder_name}' found.")
            return {"status": 404, "message": f"Noo folder with name: {list_folder} found" }
        
        images = ListImageAlone.query.filter_by(IDCategories = alone_template.id_cate).all()

        img_link = [img.image for img in images]

        return img_link
    except Exception as error:
        print("Error:", error)
        return None

    finally:
        return img_link


def get_list_categoris_alone(list_folder):
    try:
        template = AloneTemplate.query.filter_by(folder_name=list_folder).first()

        if template is None:
            print("Noo folder with name: '{folder_name}' found")
            return {"status": 404, "message": f"Noo folder with name: {list_folder} found" }
        result_dict = {
            "id_cate": template.id_cate,
            "name_cate": template.name_cate,
            "image_sample": template.image_sample,
        }
        return result_dict
    except Exception as error:
        print("Error:", error)
        return None

def get_thiep_cuoi(
    name1,
    name2,
    date,
    link_image,
    location,
    link_location,
    link_qr,
    status,
    id_user,
    link1,
    link2,
):
    try:
        new_detail = WeddingDetail(
            groom_name = name1,
            bride_name = name2,
            wedding_date = date,
            wedding_image = link_image,
            wedding_location = location,
            google_maps_link = link_location,
            qr_code_image = link_qr,
            attendance_status = status,
            id_user = id_user,
            groom_image = link1,
            bride_image = link2,
        )
        db.session.add(new_detail)
        db.session.commit()
        print("Data inserted successfully into `wedding_details` table.")

        list_detail = WeddingDetail.query.order_by(WeddingDetail.id.desc()).first()
        for item in list_detail:
        # Tạo dictionary chứa các giá trị đã lưu
            result_dict = {
                "id": item.id,
                "groom_name": item.groom_name,
                "bride_name": item.bride_name,
                "wedding_date": item.wedding_date,
                "wedding_image": item.wedding_image,
                "wedding_location": item.wedding_location,
                "google_maps_link": item.google_maps_link,
                "qr_code_image": item.qr_code_image,
                "attendance_status": item.attendance_status,
                "id_user": item.id_user,
                "groom_image": item.groom_image,
                "bride_image": item.bride_image,
            }

        return {"status": 200, "data": result_dict}
    except Exception as error:
        db.session.rollback()
        print(f"Failed to insert data into table: {error}")

def save_video_to_mysql_swap_imagevideo_mebau(
    src_image, src_video, link_vid_swap, id_user, device, ip, loai_sk
):
    generated_uuid = uuid.uuid4().int
    id_toan_bo_sk = str(generated_uuid)[-12:]
    count_comment = 0
    count_view = 0
    data = {}
    try:
        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data = {
                "id_saved": id_toan_bo_sk,
                "link_video_goc": src_video,
                "link_image": src_image,
                "link_vid_da_swap": link_vid_swap,
                "thoigian_sukien": date,
                "device_tao_vid": device,
                "ip_tao_vid": ip,
                "id_user": id_user,
                "loai_sk": loai_sk,
        }
        new_sk_mebau = SavedSKVideoImageMeBau(
            id_saved = id_toan_bo_sk,
            link_video_goc = src_video,
            link_image = src_image,
            link_video_da_swap = link_vid_swap,
            thoigian_sukien = date,
            device_them_su_kien = device,
            ip_them_su_kien = ip,
            loai_sk = loai_sk,
            id_user = id_user,
            count_comment = count_comment,
            count_view = count_view,
        )
        # add
        db.session.add(new_sk_mebau)
        # commit
        db.session.commit()
        return data
    except Exception as error:
        db.session.rollback()
        print(
            f"_____Loi exception ____ save_video_to_mysql_swap_imagevideo_mebau_____ {error}"
        )
        data = {
            "id_saved": id_toan_bo_sk,
            "link_video_goc": src_video,
            "link_image": src_image,
            "link_vid_da_swap": link_vid_swap,
            "thoigian_sukien": date,
            "device_tao_vid": device,
            "ip_tao_vid": ip,
            "id_user": id_user,
        }
    
def get_random_data_noel():
    return


def test():
    return ""
