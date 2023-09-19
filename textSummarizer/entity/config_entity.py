from dataclasses import dataclass
from pathlib import Path
from collections import namedtuple

@dataclass(frozen=True)
class DataIngestionConfig:
    root_data_dir: Path
    source_url: str
    zip_data_path: Path
    unzip_data_path: Path
    zip_data_file_name: str
# or 
# DataIngestionConfig = namedtuple('DataIngestionConfig', ["root_dir", "source_url", "zip_data_path", "unzip_data_path"])

DataValidationConfig = namedtuple("DataValidationConfig", ["dataset_full_path", "data_split_name", 
                                                           "columns_name_check", "data_type_check"])
