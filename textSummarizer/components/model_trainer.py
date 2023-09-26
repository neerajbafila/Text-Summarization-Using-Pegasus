from textSummarizer import Logger
from textSummarizer.constants import *
from textSummarizer import Configuration
from textSummarizer import ModelTrainingConfig
import torch
from datasets import load_from_disk
from transformers import TrainingArguments, Trainer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import DataCollatorForSeq2Seq
import sys

STAGE = "Model Training"

class Model_trainer:
    def __init__(self, model_training_config: ModelTrainingConfig):
        self.my_logger = Logger(CONFIG_FILE_PATH)
        self.my_logger.write_log(f"{STAGE} started")
        self.model_training_config = model_training_config
    
    def train(self):
        try: 
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            tokenizer_name = self.model_training_config.tokenizer_name
            tokenizer_path = self.model_training_config.tokenizer_path
            model_name = self.model_training_config.model_name
            model_path = self.model_training_config.model_path
            trained_model_path = self.model_training_config.trained_model_path
            train_data_path = self.model_training_config.transformed_training_data_dir
            print(model_path, trained_model_path, train_data_path)
            self.my_logger.write_log(f"Getting tokenizer from {tokenizer_path}")
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, cache_dir=tokenizer_path)
            self.my_logger.write_log(f"Getting Pretrained Model from {model_path}")
            model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=model_path)
            self.my_logger.write_log(f"Getting DataCollector")
            data_collector = DataCollatorForSeq2Seq(tokenizer, model_pegasus)
            no_train_epochs = self.model_training_config.no_epochs 

            

            # get training args
            training_args = TrainingArguments(
                output_dir=trained_model_path,
                num_train_epochs=no_train_epochs,
                weight_decay=0.01,
                per_device_train_batch_size=1,
                per_device_eval_batch_size=1,
                warmup_steps=500,
                logging_steps=10,
                evaluation_strategy="steps",
                eval_steps=500,
                save_steps=1e6,
                gradient_accumulation_steps=16)
            
            self.my_logger.write_log(f"Loading training data from {train_data_path}")
            datasets = load_from_disk(train_data_path)

            trainer = Trainer(model=model_pegasus,
                            args=training_args,
                            tokenizer=tokenizer,
                            data_collator=data_collector,
                            train_dataset=datasets['test'],
                            eval_dataset=datasets['validation'])
            
            self.my_logger.write_log(f"**************starting Model training with {no_train_epochs} epochs***************")
            trainer.train()
            self.my_logger.write_log(f"***************Model training completed*******************")
            
            # saving model and tokenizer
            model_pegasus.save_pretrained(trained_model_path, "pegasus-samsum-model")
            tokenizer.save_pretrained(tokenizer_path, "tokenizer_pegasus")
            self.my_logger.write_log(f"model saved at {trained_model_path}, tokenizer saved at {tokenizer_path}")
                            
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())

if __name__ == '__main__':

    conf = Configuration()
    ob = Model_trainer(conf.get_model_trainer_config())
    ob.train()