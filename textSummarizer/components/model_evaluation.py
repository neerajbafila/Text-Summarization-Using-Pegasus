from textSummarizer import Logger
from textSummarizer.constants import *
from ensure import ensure_annotations
from textSummarizer import ModelEvalConfig, Configuration
import sys
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm
import evaluate
import datasets
import pandas as pd

STAGE = "Model Evaluation"

class Model_evaluation:
    @ensure_annotations
    def __init__(self, model_eval_config: ModelEvalConfig):
        self.my_logger = Logger(CONFIG_FILE_PATH)
        self.my_logger.write_log(f"*************{STAGE} started ***************")
        self.model_eval_config = model_eval_config
    
    @ensure_annotations
    def generate_batch_sized_chunks(self, list_of_elements, batch_size:int):
        """split the dataset into smaller batches that we can process simultaneously
        Yield successive batch-sized chunks from list_of_elements

        Args:
            list_of_elements (_type_): text
            batch_size (_type_): size of batch
        """
        try:
            for i in range(0, len(list_of_elements), batch_size):
                yield list_of_elements[i:i + batch_size]
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())

    def calculate_metric(self, dataset, tokenizer, model, matrix, batch_size=8, col_for_text="dialogue",col_for_target="summary"):
        try:

            device = "cuda" if torch.cuda.is_available() else "cpu" 
            input_data = list(self.generate_batch_sized_chunks(dataset[col_for_text], batch_size))
            target_data = list(self.generate_batch_sized_chunks(dataset[col_for_target], batch_size))
            
            for inp_data, opt_data in tqdm(zip(input_data, target_data), total=len(input_data)):
                inputs = tokenizer(inp_data, max_length=1024, truncation=True, padding='max_length', return_tensors='pt')
                generated_opt = model.generate(input_ids=inputs['input_ids'].to(device), attention_mask=inputs['attention_mask'].to(device),
                                            length_penalty=0.8, num_beams=8, max_length=128)
                ''' parameter for length penalty ensures that the model does not generate sequences that are too long. '''
                # Finally, we decode the generated texts, 
                # replace the  token, and add the decoded texts with the references to the metric.
                decoded_texts = [tokenizer.decode(s, skip_special_tokens=True, clean_up_tokenization_spaces=True) for s in generated_opt]

                matrix.add_batch(predictions=decoded_texts, references=opt_data)

            score = matrix.compute()
            return score
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())

    def evaluate(self):
        try:
            tokenizer_path = self.model_eval_config.tokenizer_path
            model_path = self.model_eval_config.model_path
            # model_name = self.model_eval_config.model_name
            tokenizer_name = self.model_eval_config.tokenizer_name
            self.my_logger.write_log(f"getting tokenizer and model {model_path}")
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, cache_dir= tokenizer_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            eval_dataset_path = self.model_eval_config.eval_data_path
            eval_dataset = datasets.load_from_disk(eval_dataset_path)
            # eval_dataset = eval_dataset['train'][:1]
            matrix_name = self.model_eval_config.matrix_name
            matrix = evaluate.load(matrix_name)
            # (self, dataset, tokenizer, model, matrix, batch_size=3, col_for_text="dialogue",col_for_target="summary"):
            score = self.calculate_metric(dataset=eval_dataset['train'][:1], tokenizer=tokenizer, model=model, matrix=matrix, batch_size=8)
            rouge_df = pd.DataFrame(score, index=['score'])
            rouge_df.to_csv(self.model_eval_config.eval_matrix_path)
            self.my_logger.write_log(f"evaluation matrix has stored at {self.model_eval_config.eval_matrix_path}")
        except Exception as e:
            self.my_logger.write_exception(e)
            raise Exception(e, sys.exc_info())
        


    

if __name__ == '__main__':
    c = Configuration()
    ob = Model_evaluation(c.get_model_evaluation_config())
    ob.evaluate()
   