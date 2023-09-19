from textSummarizer import Configuration, DataValidationConfig
from textSummarizer.constants import * 
from textSummarizer import Logger
from datasets import load_from_disk
import sys

STAGE = "DataValidation"
class Data_validation:
    def __init__(self, data_validation_config: DataValidationConfig):
        self.my_logger = Logger(CONFIG_FILE_PATH)
        self.my_logger.write_log(f"{STAGE} started")
        self.data_validation_config = data_validation_config
    
    def load_data(self):
        try:
            data_full_path = self.data_validation_config.dataset_full_path
            data = load_from_disk(data_full_path)
            return data
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())


    def split_name_checks(self):
        data = self.load_data()
        split_name = self.data_validation_config.columns_name_check
        print(s)


c = Configuration()
ob = Data_validation(c.get_data_validation_config())
data = ob.load_data()
print(data)


