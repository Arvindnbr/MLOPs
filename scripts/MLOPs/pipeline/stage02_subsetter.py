import sys
from scripts.MLOPs.config.configuration import ConfigurationManager
from scripts.MLOPs.exception import AppException
from scripts.MLOPs import logger
from scripts.MLOPs.components.data_sorter import DataSetSorter


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



if __name__ == '__name__':
    try:
        logger.info(f">>>>>>>>>>>>>>>>> stage {STAGE1} started <<<<<<<<<<<<<<<<<")
        step1 = DataSubsetterPipeline()
        step1.main()
        logger.info(f">>>>>>>>>>>>>>>>>> stage {STAGE1} completed <<<<<<<<<<<<<<<<<<<< \n \n xxxxxxxxxxxxx=====xxxxxxxxxxxxxx")
    except Exception as e:
        raise AppException(e, sys)