import os
import json
from pathlib import Path
from pprint import pprint


BASE_DIR = Path(__file__).resolve().parent


# list_id = []

# with open(os.path.join(BASE_DIR, "data.json")) as js:
#     file = json.load(js)
#     for item in file:
#         list_id.append(item['description'].split("\n")[1].split()[1].strip())


# _id = []




# with open(os.path.join(BASE_DIR, "result.json")) as js:
#     file = json.load(js)
#     print(len(file))
#     count = 0
#     for item in file:
#         if str(item['id']).strip() in list_id: count += 1
#         _id.append(str(item["id"]).strip())

#     print(count)

# print(len(list_id))

# print(sorted(list_id)[0], sorted(_id)[-1])


# _id.extend(list_id)
# print(len(set(_id)))




with open(os.path.join(BASE_DIR, "result.json")) as js:
    file = json.load(js)
    for i in file:
        print(i["time"])


























# list_dir = os.listdir(os.path.join(BASE_DIR, "request_api"))[20000:]

# local_storage = []



# def write_file(resp, filename):
#     with open(filename, "w", encoding="utf8") as file:
#         json.dump(resp, file, indent=2, ensure_ascii=False)


# def get_data_for_parse(lst: list, path: str) -> list:
    
#     if path.split(".")[-1] == "json":
#         with open(os.path.join(BASE_DIR, "request_api/" + path)) as js:
#             file = json.load(js)
#             try:
#                 if "error" in file: return
#                 server_photo = file['response'][0]['sizes'][-1]
#                 description = file["response"][0]["text"]
#                 lst.append({
#                     "path_photo": server_photo,
#                     "description": description
#                 })                
#             except Exception as e:
#                 print("Error")
        



# for item in list_dir:
#     get_data_for_parse(local_storage, item)

# write_file(local_storage, "data.json")
