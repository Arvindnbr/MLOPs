import sys,zipfile,os
from urllib import request
from scripts.MLOPs.exception import AppException
from scripts.MLOPs import logger
from scripts.MLOPs.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    

    def download_data(self)->str:
        try:
            dataset_url = self.config.source_URL
            os.makedirs(self.config.root_dir, exist_ok= True)
            logger.info(f"Downloading data from {dataset_url} into file {self.config.local_data}")
            if not os.path.exists(self.config.local_data):
                request.urlretrieve(
                    url = dataset_url, filename=self.config.local_data
                )
                logger.info(f"{self.config.local_data} downloaded!!")
            else:
                logger.info(f"File already exists on {self.config.local_data}")
            
        
        except Exception as e:
            raise AppException(e, sys)
    
    def extract_zipfile(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path,exist_ok=True)
        with zipfile.ZipFile(self.config.local_data, 'r') as z:
            z.extractall(unzip_path)