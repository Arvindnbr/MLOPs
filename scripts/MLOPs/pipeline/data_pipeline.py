import sys
from scripts.MLOPs import logger
from scripts.MLOPs.config.configuration import ConfigurationManager
from scripts.MLOPs.exception import AppException
from scripts.MLOPs.components.data_ingestion import DataIngestion
from scripts.MLOPs.components.data_validation import DataValidation
from scripts.MLOPs.components.model_trainer import ModelTrainer
from scripts.MLOPs.components.data_sorter import DataSetSorter


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

STAGE1 = "Data Subset Creation"
#optional #can be skipped if classes is null
class DataSubsetterPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        dataset_config = config.get_Dataset_config()
        if len(dataset_config.classes) != 0:
            try:
                datasubsetter = DataSetSorter(yamlconfig=dataset_config)
                datasubsetter.create_dataset()
            except Exception as e:
                raise AppException(e, sys)
        else:
            pass


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
        model_config = config.get_train_log_config()
        valc = config.get_datavalidation_config()
        params = config.get_params()
        x = ModelTrainer(config=model_config, val=valc, param=params)
        x.run_pipeline()
        
    


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE} started <<<<<<<<<<<<<<<<<")
        step1 = DataIngestionPipeline()
        step1.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE1} started <<<<<<<<<<<<<<<<<")
        step2 = DataSubsetterPipeline()
        step2.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE1} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE2} started <<<<<<<<<<<<<<<<<")
        step3 = DataValidationPipeline()
        step3.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE2} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE3} started <<<<<<<<<<<<<<<<<")
        step4 = ModelTrainerPipeline()
        step4.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE3} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
    except Exception as e:
        logger.exception(e)
        raise AppException(e, sys)
    




    
