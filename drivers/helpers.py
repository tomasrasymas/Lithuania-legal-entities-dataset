import requests
import zipfile
from typing import List
from config import config
import os


def download_file(file_url: str, save_file_path: str) -> str:
    response = requests.get(file_url, allow_redirects=True)

    try:
        with open(save_file_path, 'wb') as f:
            f.write(response.content)
    except:
        return None
    
    return save_file_path


def unzip_file(file_path: str, file_extention: str = '.csv') -> List[str]:
    extracted_files = []
    
    with zipfile.ZipFile(file_path, 'r') as f:
        zipped_files = f.namelist()
        for zipped_file in zipped_files:
            if zipped_file.endswith(file_extention):
                extracted_file_path = os.path.join(config.DATA_PATH, zipped_file)
                f.extract(zipped_file, config.DATA_PATH)

                extracted_files.append(extracted_file_path)
    
    return extracted_files
