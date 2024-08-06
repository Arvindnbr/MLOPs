import os, re, random
import yaml
import shutil
from scripts.MLOPs import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
from typing import Any
import base64


ROOT_DIR = Path(__file__).resolve().parents[1]


@ensure_annotations
def read_yaml(yaml_path:Path)-> ConfigBox:
    try:
        with open(yaml_path) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {yaml_path} loaded sucessfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def update_train_yaml(yaml_path, path_dir):
    with open(yaml_path,'r') as file:
        data = yaml.safe_load(file)
    data['train'] = 'train/images'
    data['val'] = 'valid/images'
    new_key = 'path'
    new_value = path_dir
    data[new_key] = new_value

    with open(yaml_path, 'w') as file:
        yaml.safe_dump(data, file,default_flow_style=False)

@ensure_annotations
def create_directories(path_to_dir: list, verbose=True):
    for path in path_to_dir:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at {path}")

@ensure_annotations
def get_size(path:Path) -> str:
    size_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_kb} KB"

@ensure_annotations
def save_json(path:Path, data:dict):
    with open(path,"w") as f:
        content = json.load(f)
    logger.info(f"json file {path} loaded sucessfully")
    return ConfigBox(content)

def decodeImage(imgstr, filename):
    imgdata = base64.b64decode(imgstr)
    with open(filename, 'w') as f:
        f.write(imgdata)
        f.close()

def encodeImage(cropped_imgpath):
    with open (cropped_imgpath, 'rb') as f:
        return base64.b64encode(f.read())
    
#get the train folder from run
def get_highest_train_folder(parent_folder):
    items = os.listdir(parent_folder)
    # Filter the folders and get their numbers
    train_folders = [
        (item, int(item[5:]))
        for item in items
        if os.path.isdir(os.path.join(parent_folder, item)) and re.match(r'train\d+$', item)
    ]
    # Return the folder with the highest number, or None if no matching folders
    return max(train_folders, key=lambda x: x[1])[0] if train_folders else None



def get_random_file_from_folder(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if files:
        random_file = random.choice(files)
        return os.path.join(folder_path, random_file)
    else:
        print(f"No files found in {folder_path}.")
        return None

# def indices(base_set: list, new_set: list):
#     base_set = [item.lower() for item in base_set]
#     new_set = [item.lower() for item in new_set]
#     new_indices =[]
#     for item in new_set:
#         indices = [i for i, x in enumerate(base_set) if x == item]
#         new_indices.extend(indices)
#     return new_indices


