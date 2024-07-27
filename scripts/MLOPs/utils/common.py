import os
import yaml
from scripts.MLOPs import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path
from typing import Any
import base64




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