import time

import requests
import json

import update_last_size
import update_actual_fees
import update_albums

headers = {
    "Content-Type": "application/json"
} 

body = {
    "method": "get_product",
    "secret_key": "123123"
}

url = "http://api.vikazakazhi.ru"


def get_products(method):
    body["method"] = method
    r = requests.post(url=url, headers=headers, data=json.dumps(body)).json()
    if r['answer'] != "error":
        if r['answer'] == "Catalog":
            del r['answer']
            return r
        return r['answer']
    return False


def main():
    while True:
        data = get_products("get_product")
        if data:
            update_last_size.main(data)
            update_actual_fees.main(data)
        data = get_products("get_data_for_catalogs")
        update_albums.main(data)

        time.sleep((1 * 60) * 180)


if __name__ == "__main__":
    main()
