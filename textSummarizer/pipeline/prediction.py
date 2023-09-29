from textSummarizer import Logger, Configuration
from textSummarizer import ModelEvalConfig
from textSummarizer.constants import *
from transformers import AutoTokenizer, pipeline

STAGE = "Prediction"
class Prediction:
    def __init__(self, model_eval_config: ModelEvalConfig):
        self.my_logger = Logger(CONFIG_FILE_PATH)
        self.my_logger.write_log(f"*****{STAGE} started******")
        self.model_eval_config = model_eval_config
    
    def prediction(self, text, length_penalty=0.8, max_length=128, num_beams=8):
        gen_kwargs = {"length_penalty": length_penalty, "num_beams":num_beams, "max_length":max_length}
        tokenizer_path = self.model_eval_config.tokenizer_path
        tokenizer_name = self.model_eval_config.tokenizer_name
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, cache_dir=tokenizer_path)
        model_path = self.model_eval_config.model_path
        pipe = pipeline("summarization", model=model_path, tokenizer=tokenizer)
        # print(text)
        output = pipe(text, **gen_kwargs)
        # print(output[0]["summary_text"])
        return output[0]["summary_text"]

if __name__ == "__main__":
    conf = Configuration()
    ob = Prediction(conf.get_model_evaluation_config())
    text = """ sample text""" 
    ob.prediction(text)





