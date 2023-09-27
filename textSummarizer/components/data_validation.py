from textSummarizer import Configuration, DataValidationConfig
from textSummarizer.constants import * 
from textSummarizer import Logger
from datasets import load_from_disk
import sys
import pandas as pd
from typing import Any

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
        try:
            self.my_logger.write_log(f"validating split name of datasets")
            data = self.load_data()
            split_name = self.data_validation_config.data_split_name
            if (list(data.keys()) == split_name):
                return True
            else:
                return False
            
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
        
    def column_names_check(self):
        try:
            self.my_logger.write_log(f"validating columns names of datasets")
            data = self.load_data()
            columns_names = self.data_validation_config.columns_name_check
            split_name = self.data_validation_config.data_split_name
            column_check = []
            for s_name in split_name:
                column_check.append(pd.DataFrame(data[s_name]).columns == columns_names) # [array([ True,  True,  True]), array([ True,  True,  True]), array([ True,  True,  True])] for train, test and validation 
            column_check =  sum(column_check) # [3,3,3]
            
            if sum(column_check) == len(split_name) * len(columns_names):
                return True
            else:
                return False
            
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())

    def data_types_check(self):
        try:
            self.my_logger.write_log(f"validating data types of datasets")
            data_type = self.data_validation_config.data_type_check
            split_name = self.data_validation_config.data_split_name
            checks = False
            data = self.load_data()
            for s_name in split_name:
                if (data[s_name].features['id'].dtype==data_type[0] and data[s_name].features['dialogue'].dtype==data_type[1]
                    and data[s_name].features['summary'].dtype==data_type[2]):
                    checks = True
            return checks
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
            
    def drive_check(self):
        try:
            all_checks = []
            if self.split_name_checks():
                all_checks.append([self.split_name_checks(),
                                   self.column_names_check(),
                                   self.data_types_check()
                                   ])
                self.my_logger.write_log(f"all checks completed and result is \n{all_checks}")
                return all_checks
            else:
                self.my_logger.write_log(f"split name checks failed, not able to initiated others checks")
                all_checks.append([False])
                return all_checks
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())

# if __name__ == "__main__":
#     c = Configuration()
#     ob = Data_validation(c.get_data_validation_config())
#     c = ob.drive_check()
#     print(c)



