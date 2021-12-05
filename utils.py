import json
from datetime import datetime
import requests
import time
from models import LastSize, ActualFees, AlbumVk, db
import data_for_vk


MODELS = {
    "last_size": LastSize,
    "actual_fees": ActualFees,
    "albums": AlbumVk
}


def create_line_size(size):
    line_size = ""
    for s in size: line_size += f" {s},"
    return line_size


def create_values(id_prod, data_prod):
    kwargs = {
        "id": id_prod,
        "description": data_prod['description'],
        "price": data_prod['price'],
        "size": create_line_size(data_prod['size'])
    }
    return kwargs


def create_description(kwargs):
    template_string = "Ссылка: https://vikazakazhi.ru/fees/{id}  \nId: {id} \nОписание:" \
                      " {description} \nЦена: {price} \nСвободные размеры: {size}".format(**kwargs)
    return template_string


def create_description_for_album(kwargs):
    template_string = "Ссылка: https://vikazakazhi.ru/category/{id}  \nId: {id} \nОписание:" \
                      " {description} \nЦена: {price} \nСвободные размеры: {size}".format(**kwargs)
    return template_string


def write_file(resp, filename):
    with open(filename, "w", encoding="utf8") as file:
        json.dump(resp, file, indent=2, ensure_ascii=False)


def delete_product_in_vk(lst, flag_for_model):
    url = data_for_vk.url_vk
    params = data_for_vk.params_for_vk
    try:
        for item in lst:
            time.sleep(1)
            params["owner_id"], params["photo_id"] = int(item.owner_id), item.photo_id
            resp = requests.get(url=url.format("photos.delete"), params=params).json()
            write_file(resp, f"request_api/{str(int(time.time()))}.json")
            if resp['response']:
                try:
                    MODELS[flag_for_model].delete().where(MODELS[flag_for_model].id_product == item.id_product).execute()
                except Exception as e:
                    print(e)
                    db.rollback()
    except Exception as e:
        print(e)


def get_upload_server(slug):
    params = data_for_vk.params_for_vk
    params["group_id"], params["album_id"] = data_for_vk.group_id, data_for_vk.albums_id[slug]
    resp = requests.get(url=data_for_vk.url_vk.format("photos.getUploadServer"), params=params).json()
    write_file(resp, f"request_api/{str(int(time.time()))}.json")
    print(resp)
    return resp["response"]["upload_url"]


def send_photo(upload_url, img_path):
    file = {"file1": open(img_path, 'rb')}
    resp = requests.post(url=upload_url, files=file).json()
    write_file(resp, f"request_api/{str(int(time.time()))}.json")
    return resp


def save_photo_in_vk(data_for_save, description):
    resp = requests.get(url=data_for_vk.url_vk.format("photos.save"), params={
                                                        "access_token": data_for_vk.params_for_vk['access_token'],
                                                        "group_id": data_for_save["gid"],
                                                        "album_id": data_for_save["aid"],
                                                        "photos_list": data_for_save["photos_list"],
                                                        "description": description,
                                                        "server": data_for_save["server"],
                                                        "hash": data_for_save["hash"],
                                                        "v": data_for_vk.params_for_vk["v"]
                                                            }).json()

    write_file(resp, f"request_api/{str(int(time.time()))}.json")
    return resp


def save_photo(photo):
    time.sleep(1)
    with open("img.jpg", "wb") as file:
        file.write(photo)


def parse_url_img(img_path):
    base_url = "https://vikazakazhi.ru/"
    if img_path[0] == "s":
        return base_url + img_path
    return base_url + "static/" + img_path


def download_photo(path):
    img = requests.get(path)
    save_photo(img.content)


def update_model(id_prod, save_data, slug):
    try:

        MODELS[slug].create(
            product_id=int(id_prod),
            owner_id=str(save_data['response'][0]['owner_id']),
            photo_id=int(save_data['response'][0]['id'])
        )
        print("access create")
    except Exception as e:
        print("False create model")
        print(e)
        db.rollback()


def update_model_albums(id_prod, save_data):
    try:
        AlbumVk.create(
            product_id=int(id_prod),
            owner_id=str(save_data['response'][0]['owner_id']),
            photo_id=int(save_data['response'][0]['id']),
            create_at=datetime.now()
        )
    except Exception as e:
        print("error create model album")
        print(e)
        db.rollback()


def send_photo_in_vk(lst_product, slug):
    for product in lst_product:
        download_photo(parse_url_img(lst_product[product]['photo']))
        result_send = send_photo(get_upload_server(slug), "img.jpg")
        if "error" in result_send: continue
        else:
            result_save = save_photo_in_vk(
                result_send,
                create_description(create_values(product, lst_product[product]))
            )
            if "error" in result_save: continue
            update_model(product, result_save, slug)


def send_photo_in_albums(lst_prod, id_album):
    for prod in lst_prod:
        download_photo(parse_url_img(prod['img']))
        data_for_vk.albums_id['catalog'] = int(id_album)
        result_send = send_photo(get_upload_server("catalog"), "img.jpg")
        if "error" in result_send: continue
        else:
            result_save = save_photo_in_vk(
                result_send,
                create_description_for_album(create_values(prod['id'], prod))
            )
        if "error" in result_save: continue
        update_model_albums(prod['id'], result_save)
        print("phot upload")
