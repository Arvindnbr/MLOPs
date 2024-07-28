from scripts.MLOPs import logger
import sys
from scripts.MLOPs.exception import AppException
from scripts.MLOPs.pipeline.data_pipeline import DataIngestionPipeline,DataValidationPipeline

STAGE = "Data Ingestion"
STAGE2 = "Data Validation Stage"

try:
    logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE} started <<<<<<<<<<<<<<<<<")
    obj = DataIngestionPipeline()
    obj.main()
    logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
    logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE2} started <<<<<<<<<<<<<<<<<")
    obj1 = DataValidationPipeline()
    obj1.main()
    logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE2} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
except Exception as e:
    logger.exception(e)
    raise AppException(e, sys)