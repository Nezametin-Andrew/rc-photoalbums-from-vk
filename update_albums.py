from models import db, AlbumVk
from utils import send_photo_in_albums


def sort_and_upload(data, list_id):
    up_data = {}
    for key in data:
        for items in data[key]:
            up_data[items["id_album"]] = []
            for item in items['product_list']:
                if int(item['id']) in list_id: continue
                up_data[items['id_album']].append(item)
            print(len(up_data[items["id_album"]]))
            send_photo_in_albums(up_data[items['id_album']], items['id_album'])


def get_data_from_vk():
    try:
        prod = AlbumVk.select()
        return prod
    except Exception as e:
        print(e)
        db.rollback()
        return None


def get_actual_product(data):
    result_data = {}
    for key in data:
        result_data[key] = []
        for items in data[key]:
            if items['product_list']:
                print(items['title'])
                print(len(items['product_list']))
                result_data[key].append(items)
    return result_data


def main(data):
    actual_data = get_actual_product(data)
    get_prod_in_vk = get_data_from_vk()
    sort_and_upload(actual_data, [i.product_id for i in get_prod_in_vk])
