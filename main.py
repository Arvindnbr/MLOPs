from scripts.MLOPs import logger
import sys
from scripts.MLOPs.exception import AppException
from scripts.MLOPs.pipeline.stage01_data_ingestion import DataIngestionPipeline

STAGE = "Data Ingestion"

try:
    logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE} started <<<<<<<<<<<<<<<<<")
    obj = DataIngestionPipeline()
    obj.main()
    logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
except Exception as e:
    logger.exception(e)
    raise AppException(e, sys)