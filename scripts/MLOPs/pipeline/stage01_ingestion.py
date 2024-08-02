from scripts.MLOPs import logger
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
