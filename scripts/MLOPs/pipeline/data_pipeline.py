import sys,os
from scripts.MLOPs import logger
from scripts.MLOPs.config.configuration import ConfigurationManager
from scripts.MLOPs.exception import AppException
from scripts.MLOPs.components.data_ingestion import DataIngestion
from scripts.MLOPs.components.data_validation import DataValidation
from scripts.MLOPs.components.model_trainer import ModelTrainer


STAGE = "Data Ingestion stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
            config = ConfigurationManager()
            dataingestion_config = config.get_dataingestion_config()
            dataingestion = DataIngestion(config=dataingestion_config)
            dataingestion.download_data()
            dataingestion.extract_zipfile()


STAGE2 = "Data Validation Stage"

class DataValidationPipeline:
    def __init__(self) -> None:
         pass
    
    def main(self):
        config = ConfigurationManager()
        dataval_param = config.get_dataingestion_config()
        dataval_config = config.get_datavalidation_config()
        data_validation = DataValidation(config=dataval_config, param=dataval_param)
        data_validation.validate_files()
        data_validation.update_yaml()
        
STAGE3 = "Model Trainer"

class ModelTrainerPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        model_config = config.get_model_trainer()
        dirc = config.get_dataingestion_config()
        valc = config.get_datavalidation_config()
        mlflowc = config.get_mlflow_config()
        x = ModelTrainer(config=model_config, dir=dirc, val=valc, mlflow=mlflowc)
        x.run_pipeline()
    


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE} started <<<<<<<<<<<<<<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE2} started <<<<<<<<<<<<<<<<<")
        obj1 = DataValidationPipeline()
        obj1.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE2} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE3} started <<<<<<<<<<<<<<<<<")
        obj1 = ModelTrainerPipeline()
        obj1.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE3} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
    except Exception as e:
        logger.exception(e)
        raise AppException(e, sys)