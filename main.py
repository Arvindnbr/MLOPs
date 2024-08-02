from scripts.MLOPs import logger
import sys
from scripts.MLOPs.exception import AppException
from scripts.MLOPs.pipeline.stage01_ingestion import DataIngestionPipeline
from scripts.MLOPs.pipeline.stage02_subsetter import DataSubsetterPipeline
from scripts.MLOPs.pipeline.stage03_validation import DataValidationPipeline
from scripts.MLOPs.pipeline.stage04_trainer import ModelTrainerPipeline


STAGE = "Data Ingestion"
STAGE1 = "Data Subset Creation"
STAGE2 = "Data Validation"
STAGE3 = "Model Trainer"


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