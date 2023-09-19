import os
import sys
from box.exceptions import BoxValueError
import yaml
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import List
from datetime import datetime

@ensure_annotations
def read_yaml(path_to_yaml: Path=Path("config/config.yaml")) ->ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml(str): path os yaml file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            return ConfigBox(content)
    except BoxValueError as bv:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(dirs:List):
    """create directories from given list of directories

    Args:
        dirs (List): list of directories to be created
    """
    try:
        full_dir_path = ""
        for dir in dirs:
            full_dir_path = os.path.join(full_dir_path, dir)
        os.makedirs(full_dir_path,exist_ok=True)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_no = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f"Exception occurred \nexc_type {exc_type}, exc_obj {exc_obj}, line_no {line_no}, file_name {file_name}")

@ensure_annotations
def get_unique_name()->str:
    now = datetime.now()
    name = now.strftime("%d-%m-%Y")
    return name

@ensure_annotations
def get_size(path: Path):
    size_in_kb = round(os.path.getsize(path)/1024)
    return size_in_kb