from scripts.MLOPs import logger
from scripts.MLOPs.config.configuration import ConfigurationManager
from scripts.MLOPs.components.data_validation import DataValidation


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