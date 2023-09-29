from textSummarizer import Logger
from textSummarizer import DataPreprationConfig
from ensure import ensure_annotations
from textSummarizer.constants import *
from textSummarizer import Configuration
from datasets import load_from_disk
from transformers import AutoTokenizer
import sys


STAGE = "Data_Prepration"
class Data_prepration:
    @ensure_annotations
    def __init__(self, data_prepration_config: DataPreprationConfig):
        self.my_logger = Logger(CONFIG_FILE_PATH)
        self.my_logger.write_log(f"*********{STAGE} started*************")
        self.data_prepration_config = data_prepration_config
    
    def load_data(self):
        try:   
            self.my_logger.write_log(f"loading raw data for transformation")
            unzip_data_path = self.data_prepration_config.unzip_data_path
            data = load_from_disk(unzip_data_path)
            return data
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())

    def convert_examples_to_features(self, example_batch):
        try:    
            tokenizer_path = self.data_prepration_config.tokenizer_path
            example_batch = example_batch
            tokenizer_name = self.data_prepration_config.tokenizer_name
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, cache_dir=tokenizer_path)
            input_encodings = tokenizer(example_batch['dialogue'], max_length=1024, truncation=True)
            # for labels
            with tokenizer.as_target_tokenizer():
                target_encodings = tokenizer(example_batch['summary'], max_length=128, truncation=True)
            
            return {
                "input_ids": input_encodings['input_ids'],
                "attention_mask": input_encodings['attention_mask'],
                "labels": target_encodings["input_ids"],
            }
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
        
    def convert_data(self):
        try:
            prepared_data_path = self.data_prepration_config.transformed_data_dir
            data  = self.load_data()
            self.my_logger.write_log(f"tokenizing data")
            converted_dataset = data.map(self.convert_examples_to_features, batched=True)
            converted_dataset.save_to_disk(prepared_data_path)
            self.my_logger.write_log(f"tokenized data have saved at {prepared_data_path}")
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())

if __name__ == "__main__":
    ob_c = Configuration()
    ob = Data_prepration(ob_c.get_data_prepration_config())
    ob.convert_data()