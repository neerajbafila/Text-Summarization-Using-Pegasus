from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("config/params.yaml")

PATHS_KEY = "paths"
LOGS_FOLDER_NAME_KEY = "logs"
LOGS_FILE_NAME_KEY = "logs_file_name"
SOURCE_URL_KEY = "source_url"
ZIP_DATA_PATH_KEY = "zip_data_path"
ZIP_DATA_FILE_NAME_KEY = "zip_data_file_name"
UNZIP_DATA_PATH_KEY = "unzip_data_path"
DATASET_NAME_KEY = "data_set_name"


DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_SPLIT_NAME_KEY = "data_split_name"
COLUMN_NAME_CHECK_KEY = "column_name_check"
DATA_TYPE_CHECK_KEY = "data_type_check"

DATA_PREPRATION_KEY= "data_prepration"
ROOT_DIR_KEY = "root_dir"
TRANSFORMED_DATA_DIR_KEY = "transformed_data_dir"
TOKENIZER_NAME_KEY = "tokenizer_name"
TOKENIZER_PATH_KEY = "tokenizer_path"

TRAININGARGUMENTS_KEY = "TrainingArguments"
NUM_TRAIN_EPOCHS_KEY = "num_train_epochs"
