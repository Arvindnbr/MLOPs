import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


project_name = 'MLOPs'

list_of_files = [
    ".github/workflows/.gitkeep",
    f"scripts/{project_name}/__init__.py",
    f"scripts/{project_name}/components/__init__.py",
    f"scripts/{project_name}/utils/__init__.py",
    f"scripts/{project_name}/config/__init__.py",
    f"scripts/{project_name}/config/configuration.py",
    f"scripts/{project_name}/pipeline/__init__.py",
    f"scripts/{project_name}/entity/__init__.py",
    f"scripts/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "research/trials.ipynb",
    "templates/index.html",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",

    ]

for file in list_of_files:
    filepath = Path(file)
    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,'w') as file:
            pass
            logging.info(f"creating empty file: {filepath}")
    
    else:
        logging.info(f"{filename} already exists")
                     