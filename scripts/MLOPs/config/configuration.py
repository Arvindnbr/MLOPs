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
            current_dset= config.current_dset,
            root_dir=config.data_val_dir,
            status_file_dir= config.data_val_status,
            req_files= config.data_val_req
            )
        return data_validation_config
    
    def get_train_log_config(self)-> TrainLogConfig:
        config = self.config.train_log_config
        trainlogconfig = TrainLogConfig(
            model= config.model,
            save_path= config.save_path,
            mlflow_uri= config.mlflow_uri,
            experiment_name= config.experiment_name,
            model_name= config.model_name
            )
        return trainlogconfig
    
    #optional
    def get_Dataset_config(self)-> DataSetConfig:
        config = self.config.custom_dataset
        dataset_config = DataSetConfig(
            base_Data_path= config.base_Data_path,
            classes= config.classes,
            new_data_path= config.new_data_path,
            dataset_name=config.dataset_name
        )
        return dataset_config
    
    def get_params(self)-> Params:
        param = self.config.param
        params = Params(
            optimizer = param.optimizer,
            lr0 = param.lr0,
            save_period = param.save_period,
            batch = param.batch,
            epochs = param.epochs,
            resume = param.resume,
            seed = param.seed,
            imgsz = param.imgsz
        )
        return params
    