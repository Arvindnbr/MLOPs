from scripts.MLOPs import logger
import sys
from scripts.MLOPs.exception import AppException
from scripts.MLOPs.config.configuration import ConfigurationManager
from scripts.MLOPs.components.data_validation import DataValidation


STAGE2 = "Data Validation Stage"

class DataValidationPipeline:
    def __init__(self) -> None:
         pass
    
    def main(self):
        config = ConfigurationManager()
        dataval_config = config.get_datavalidation_config()
        data_validation = DataValidation(config=dataval_config)
        data_validation.validate_files()
        data_validation.update_yaml()

if __name__ == '__main__':
    try:
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE2} started <<<<<<<<<<<<<<<<<")
        step1 = DataValidationPipeline()
        step1.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE2} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
    except Exception as e:
        raise AppException(e, sys)