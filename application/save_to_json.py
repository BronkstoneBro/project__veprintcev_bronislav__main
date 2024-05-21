import json
import os

from urllib.parse import urlparse



def save_to_json(data, folder_path, url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname.replace('.', '_')
    filename = f"{hostname}_{parsed_url.path.replace('/', '_')}_products.json"
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Данные сохранены в файл '{filename}' в папке '{folder_path}'.")


