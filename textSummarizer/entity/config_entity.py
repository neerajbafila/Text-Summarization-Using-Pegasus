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

@dataclass(frozen=True)
class DataPreprationConfig:
    unzip_data_path: Path
    root_dir: Path
    transformed_data_dir: Path
    tokenizer_name: Path
    tokenizer_path: Path

ModelTrainingConfig = namedtuple("ModelTrainingConfig", ["model_name", "model_path", 
                                                         "tokenizer_name", "tokenizer_path",
                                                         "transformed_training_data_dir",
                                                         "trained_model_path",
                                                         "no_epochs"
                                                         ])

@dataclass(frozen=True)
class ModelEvalConfig:
    matrix_name: str
    eval_data_path: Path
    model_name: str
    model_path: Path
    tokenizer_name: str
    tokenizer_path: Path
    # eval_matrix_name: str
    eval_matrix_path: Path
