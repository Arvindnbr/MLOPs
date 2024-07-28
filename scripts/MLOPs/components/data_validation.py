import os,sys
from scripts.MLOPs import logger
from scripts.MLOPs.exception import AppException
from scripts.MLOPs.utils.common import update_train_yaml
from scripts.MLOPs.config.configuration import DataIngestionConfig,DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig, param: DataIngestionConfig):
        self.config = config
        self.param = param

    def validate_files(self)-> bool:
        try:
            validation_status = None
            all_files = os.listdir(self.param.unzip_dir)

            os.makedirs(self.config.root_dir, exist_ok=True)

            for file in all_files:
                if file not in self.config.req_files:
                    validation_status = False
                    with open(self.config.status_file_dir,'w') as f:
                        f.write(f"validation_status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.status_file_dir, 'w') as f:
                        f.write(f"validation_status: {validation_status}")
            print(all_files)
            return validation_status
        except Exception as e:
            raise AppException(e,sys)
        
    def update_yaml(self):
        yamlpath = os.path.join(self.param.unzip_dir,"data.yaml")
        pathdir = self.param.unzip_dir
        update_train_yaml(yamlpath,pathdir)
        logger.info(f"following changes has been made \n train and valid path inside data.yaml has been modified \n path : {pathdir} has been added to data.yaml file ")
       
    
        
