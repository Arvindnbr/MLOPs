import sys
from scripts.MLOPs import logger
from scripts.MLOPs.exception import AppException
from scripts.MLOPs.config.configuration import ConfigurationManager
from scripts.MLOPs.components.data_ingestion import DataIngestion



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


if __name__ == '__main__':
    try:
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE} started <<<<<<<<<<<<<<<<<")
        step1 = DataIngestionPipeline()
        step1.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
    except Exception as e:
        raise AppException(e, sys)

