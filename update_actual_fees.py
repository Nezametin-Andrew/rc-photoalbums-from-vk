from models import ActualFees, db
from update_last_size import sort_data, get_update_data
import utils


def get_data_from_table():
    try:
        actual_fees = ActualFees.select()
        return actual_fees
    except Exception as e:
        print(e)
        db.rollback()


def get_id_actual_fees(data):
    id_lst = [item for item in data if len(data[item]['size']) > 1]
    return id_lst


def main(data):
    id_actual_fees = get_id_actual_fees(data)
    upload_data, delete_data = sort_data(id_actual_fees, ActualFees)
    upload_data = get_update_data(data, upload_data)
    utils.delete_product_in_vk(delete_data, "actual_fees")
    utils.send_photo_in_vk(upload_data, "actual_fees")
