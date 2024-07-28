from scripts.MLOPs.constants import *
from scripts.MLOPs.utils.common import read_yaml, create_directories
from scripts.MLOPs.entity.config_entity import *

class ConfigurationManager:
    def __init__(self,config_filepath = CONFIG_FILE_PATH, params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_dataingestion_config(self)-> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_URL= config.source_URL,
            local_data= config.local_data,
            unzip_dir= config.unzip_dir
            )
        return data_ingestion_config
    
    def get_datavalidation_config(self)->DataValidationConfig:
        config = self.config.data_validation
        create_directories([config.data_val_dir])
        data_validation_config = DataValidationConfig(
            root_dir=config.data_val_dir,
            status_file_dir= config.data_val_status,
            req_files= config.data_val_req
            )
        return data_validation_config
    
    def get_model_trainer(self)-> ModelTrainerConfig:
        config = self.config.training_params
        modelparams = ModelTrainerConfig(
            model= config.model,
            epoch= config.epoch,
            batch= config.batch,
            imgsz= config.imgsz
        )
        return modelparams