from textSummarizer import Logger, Configuration
from textSummarizer.constants import *
from textSummarizer.components.data_ingestion import DataIngestion
from textSummarizer.components.data_validation import Data_validation
from textSummarizer.components.data_prepration import Data_prepration
from textSummarizer.components.model_trainer import Model_trainer
from textSummarizer.components.model_evaluation import Model_evaluation
import sys

STAGE = "Training Pipeline"
class TrainingPipeline:
    def __init__(self, config_ob: Configuration):
        self.my_logger = Logger(CONFIG_FILE_PATH)
        self.my_logger.write_log(f"=========={STAGE} started========")
        self.config_ob = config_ob
    
    def run_data_ingestion(self):
        try: 
            data_ingestion_ob = DataIngestion(self.config_ob.get_data_ingestion_config())
            data_ingestion_ob.get_data()
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
    
    def run_data_validation(self):
        try:
            data_validation_ob = Data_validation(self.config_ob.get_data_validation_config())
            all_checks = data_validation_ob.drive_check()
            return all_checks
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
    
    def run_data_preparation(self):
        try:
            data_preparation_ob = Data_prepration(self.config_ob.get_data_prepration_config())
            data_preparation_ob.convert_data()
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
    
    def run_model_training(self):
        try:
            model_training_ob = Model_trainer(self.config_ob.get_model_trainer_config())
            model_training_ob.train()
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
    
    def run_model_evaluation(self):
        try:
            model_eval_ob = Model_evaluation(self.config_ob.get_model_evaluation_config())
            model_eval_ob.evaluate()
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
    
    def run_training_pipeline(self):
        try:
            self.run_data_ingestion()
            checks = self.run_data_validation()
            if sum(checks[0]) == 3:
                self.run_data_preparation()
                self.run_model_training()
                self.run_model_evaluation()
            else:
                self.my_logger.write_log(f"checks failed {checks}")
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
           
if __name__ == '__main__':
    conf = Configuration()
    train_pipeline = TrainingPipeline(conf)
    train_pipeline.run_training_pipeline()