from models import LastSize
import utils


def get_data_in_vk(model):
    try:
        list_id = model.select()
        return list_id
    except Exception as e:
        print(e)
        return False


def sort_data(data, model):
    list_id_in_vk = get_data_in_vk(model)
    delete_list = []
    if list_id_in_vk:
        for item in list_id_in_vk:
            if str(item.product_id) in data:
                index_el = data.index(str(item.product_id))
                data.pop(index_el)
            else:
                delete_list.append(item)
    return data, delete_list


def get_id_last_size(data):
    data = [item for item in data if len(data[item]['size']) == 1]
    return data


def get_update_data(data, leave_data):
    update_data = {}
    for i in leave_data:
        update_data[i] = data[i]
    return update_data


def main(data):
    id_last_size = get_id_last_size(data)
    upload_data, delete_data = sort_data(id_last_size, LastSize)
    upload_data = get_update_data(data, upload_data)
    utils.delete_product_in_vk(delete_data, "last_size")
    utils.send_photo_in_vk(upload_data, "last_size")



