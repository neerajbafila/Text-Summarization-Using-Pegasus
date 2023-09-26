from textSummarizer import Logger
from textSummarizer import DataIngestionConfig
from textSummarizer import Configuration
from textSummarizer.constants import *
from textSummarizer import create_directories, get_size
from ensure import ensure_annotations
import os, sys, zipfile
import urllib.request as request

STAGE = "DataIngestion"

class DataIngestion:
    @ensure_annotations
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        self.my_logger = Logger(CONFIG_FILE_PATH)
        self.my_logger.write_log(f"{STAGE} started")
        self.data_ingestion_config  = data_ingestion_config
    
    def download_data(self):
        try:
            zip_data_file_name = self.data_ingestion_config.zip_data_file_name
            zip_data_path = self.data_ingestion_config.zip_data_path
            create_directories([zip_data_path])
            source_url = self.data_ingestion_config.source_url            
            zip_data_path = Path(os.path.join(zip_data_path, zip_data_file_name))
            if not os.path.exists(zip_data_path):
                filename, headers = request.urlretrieve(source_url, zip_data_path)
                self.my_logger.write_log(f"data has downloaded at {zip_data_path}")
            else:
                size_of_dir = get_size(zip_data_path)
                self.my_logger.write_log(f"data already present at {zip_data_path} and size of data is {size_of_dir} KB")
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
    
    def extract_zip_file(self):
        try:
            zip_data_file_name = self.data_ingestion_config.zip_data_file_name
            zip_data_path = self.data_ingestion_config.zip_data_path
            zip_data_path = Path(os.path.join(zip_data_path, zip_data_file_name))
            unzip_data_path = self.data_ingestion_config.unzip_data_path
            create_directories([unzip_data_path])
            self.my_logger.write_log(f"Unzipping data file")
            with zipfile.ZipFile(zip_data_path, 'r') as zip_file_r:
                zip_file_r.extractall(unzip_data_path)
            self.my_logger.write_log(f"data has been extracted at {unzip_data_path} directory")
            return unzip_data_path
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
    
    def get_data(self):
        try:
            self.download_data()
            unzip_data_dir = self.extract_zip_file()
            return unzip_data_dir
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())

if __name__ == '__main__':

    conf = Configuration()
    ob = DataIngestion(conf.get_data_ingestion_config())
    d = ob.get_data()
    print(d)