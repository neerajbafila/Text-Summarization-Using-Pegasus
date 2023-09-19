import logging
import sys
from pathlib import Path
import os
from ensure import ensure_annotations
from textSummarizer.constants import *
from textSummarizer.utils.common import read_yaml, create_directories, get_unique_name

class Logger:
    @ensure_annotations
    def __init__(self, config_file_path:Path=CONFIG_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.log_file_location = self.config[PATHS_KEY][LOGS_FOLDER_NAME_KEY]
        create_directories([self.log_file_location])
        self.logs_file_name = self.config[PATHS_KEY][LOGS_FILE_NAME_KEY]
        self.log_file_unique_name = get_unique_name()
        self.log_file_unique_name = f"{self.logs_file_name}_{self.log_file_unique_name}"
        self.log_file_full_path = os.path.join(self.log_file_location, self.log_file_unique_name)
    
    @ensure_annotations
    def write_log(self, msg:str, log_level="INFO"):
        # get logger
        self.my_logger = logging.getLogger(__name__)
        self.log_level = log_level

        # set handler 
        self.file_handler = logging.FileHandler(self.log_file_full_path)
        self.console_handler = logging.StreamHandler(sys.stdout)

        # set log level
        self.my_logger.setLevel(log_level.upper())

        # define formatter
        self.log_formatter = logging.Formatter("[%(asctime)s- %(levelname)s- %(module)s]: \n<START>\t %(message)s\t<END>\n")
        self.log_formatter_console = logging.Formatter("[%(asctime)s- %(levelname)s- %(module)s]:  %(message)s")
        # add handler to handler
        self.file_handler.setFormatter(self.log_formatter)
        self.console_handler.setFormatter(self.log_formatter_console)

        # add handler to logger
        self.my_logger.addHandler(self.file_handler)
        self.my_logger.addHandler(self.console_handler)

        if self.log_level.upper()=='INFO':
            self.my_logger.info(msg)
        elif self.log_level.upper()=='WARNING':
            self.my_logger.warning(msg)
        elif self.log_level.upper()=='DEBUG':
            self.my_logger.debug(msg)
        # elif self.log_level.upper()=='ERROR':
        #     self.my_logger.error(msg)
        else:
            self.my_logger.info(msg)

        # remove exiting handler when job finished as if you call method seconde time it will write it no of time it was previously called or duplicate msg
        self.my_logger.removeHandler(self.file_handler)
        self.my_logger.removeHandler(self.console_handler)

    @ensure_annotations
    def write_exception(self, exception, log_level="ERROR"):
        # get logger
        self.my_logger = logging.getLogger(__name__)
        self.log_level = log_level

        # set handler
        self.file_handler = logging.FileHandler(self.log_file_full_path)
        self.console_handler = logging.StreamHandler(sys.stdout)

        # sel log level
        self.my_logger.setLevel(self.log_level.upper())

        # define format of log
        self.log_formate_file = logging.Formatter("[%(asctime)s- %(levelname)s- %(module)s]-\n<START>\t %(message)s\t<END>\n")
        self.log_formate_console = logging.Formatter("[%(asctime)s- %(levelname)s- %(module)s]:  %(message)s")

        # add formatter in handler
        self.file_handler.setFormatter(self.log_formate_file)
        self.console_handler.setFormatter(self.log_formate_console)

        # add handler to logger
        self.my_logger.addHandler(self.file_handler)
        self.my_logger.addHandler(self.console_handler)
        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_no = exc_tb.tb_lineno
        filename = exc_tb.tb_frame.f_code.co_filename
        msg = (f"Exception occurred {exception} \ndetails are below:\nexc_type {exc_type}, exc_obj {exc_obj}, line_no {line_no}, file_name {filename}")
        self.my_logger.error(msg)
        self.my_logger.removeHandler(self.file_handler)
        self.my_logger.removeHandler(self.console_handler)



