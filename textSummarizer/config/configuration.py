from textSummarizer.constants import *
from textSummarizer import Logger
from textSummarizer import DataIngestionConfig, DataValidationConfig, DataPreprationConfig
from textSummarizer import read_yaml, create_directories
from ensure import ensure_annotations
import os, sys
from pathlib import Path

from textSummarizer.constants.ROO_DATA_DIR_KEY import ROO_DATA_DIR_KEY

class Configuration:
    def __init__(self):
        self.my_logger = Logger(CONFIG_FILE_PATH)
        try:
            self.my_logger.write_log(f"Reading configuration file")
            self.config = read_yaml(CONFIG_FILE_PATH)
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
    @ensure_annotations
    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:

            self.my_logger.write_log(f"Getting data ingestion config details")
            root_data_dir = Path(self.config[PATHS_KEY][ROO_DATA_DIR_KEY])
            zip_data_path = Path(os.path.join(root_data_dir), self.config[PATHS_KEY][ZIP_DATA_PATH_KEY])
            unzip_data_path = Path(os.path.join(root_data_dir), self.config[PATHS_KEY][UNZIP_DATA_PATH_KEY])
            source_url = self.config[PATHS_KEY][SOURCE_URL_KEY]
            zip_data_file_name =  self.config[PATHS_KEY][ZIP_DATA_FILE_NAME_KEY]
            data_ingestion_config = DataIngestionConfig(root_data_dir=root_data_dir, zip_data_path=zip_data_path, 
                                                    unzip_data_path=unzip_data_path, source_url=source_url,
                                                    zip_data_file_name=zip_data_file_name)
            return data_ingestion_config
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())

    @ensure_annotations    
    def get_data_validation_config(self)->DataValidationConfig:
        root_data_dir = Path(self.config[PATHS_KEY][ROO_DATA_DIR_KEY])
        unzip_data_path = Path(os.path.join(root_data_dir), self.config[PATHS_KEY][UNZIP_DATA_PATH_KEY])
        dataset_full_path = Path(os.path.join(unzip_data_path, self.config[PATHS_KEY][DATASET_NAME_KEY]))
        data_split_name = self.config[DATA_VALIDATION_CONFIG_KEY][DATA_SPLIT_NAME_KEY]
        column_name_check = self.config[DATA_VALIDATION_CONFIG_KEY][COLUMN_NAME_CHECK_KEY]
        data_type_check = self.config[DATA_VALIDATION_CONFIG_KEY][DATA_TYPE_CHECK_KEY]
        data_validation_config = DataValidationConfig(dataset_full_path=dataset_full_path, data_split_name=data_split_name,
                                                      columns_name_check=column_name_check, data_type_check=data_type_check)
        return data_validation_config
    
    @ensure_annotations
    def get_data_prepration_config(self)->DataPreprationConfig:
        root_data_dir = self.config[PATHS_KEY][ROO_DATA_DIR_KEY]
        create_directories([root_data_dir])
        unzip_data_path = self.config[PATHS_KEY][UNZIP_DATA_PATH_KEY]
        unzip_data_path = Path(os.path.join(root_data_dir, unzip_data_path))
        unzip_data_full_path = Path(os.path.join(unzip_data_path, self.config[PATHS_KEY][DATASET_NAME_KEY]))
        root_dir = self.config[DATA_PREPRATION_KEY][ROOT_DIR_KEY]
        transformed_data_dir = self.config[DATA_PREPRATION_KEY][TRANSFORMED_DATA_DIR_KEY]
        transformed_data_dir = Path(os.path.join(root_dir, transformed_data_dir))
        tokenizer_name = self.config[DATA_PREPRATION_KEY][TOKENIZER_NAME_KEY]
        tokenizer_path = Path(os.path.join(self.config[DATA_PREPRATION_KEY][ROOT_DIR_KEY], self.config[DATA_PREPRATION_KEY][TOKENIZER_PATH_KEY]))
        create_directories([tokenizer_path])
        data_prepration_config = DataPreprationConfig(unzip_data_path=unzip_data_full_path, root_dir=root_dir, tokenizer_name=tokenizer_name,
                                                      transformed_data_dir=transformed_data_dir, tokenizer_path=tokenizer_path)
        return data_prepration_config


if __name__ == '__main__':


    ob = Configuration()
    # c = ob.get_data_ingestion_config()
    # c = ob.get_data_validation_config()
    c = ob.get_data_prepration_config()
    print(c)
