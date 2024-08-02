from scripts.MLOPs.exception import AppException
from scripts.MLOPs import logger
import sys
from scripts.MLOPs.config.configuration import ConfigurationManager
from scripts.MLOPs.components.model_trainer import ModelTrainer


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

if __name__ == '__main__':
    try:
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE3} started <<<<<<<<<<<<<<<<<")
        step1 = ModelTrainerPipeline()
        step1.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE3} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
    except Exception as e:
        raise AppException(e, sys)


