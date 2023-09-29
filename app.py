from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from fastapi.responses import Response, RedirectResponse
import uvicorn
import os,sys
from textSummarizer import Configuration
from textSummarizer.pipeline.training_pipeline import TrainingPipeline
from textSummarizer.pipeline.prediction import Prediction


app = FastAPI()

@app.get("/", tags=["Home"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train", tags=["Training"])
async def training():
    try:
        print('ffff')
        conf = Configuration()
        obj = TrainingPipeline(conf)
        obj.run_training_pipeline()
        return Response("Training completed successfully")
    except Exception as e:
        return Response(f"Error Occurred! {e, sys.exc_info()}")

@app.post("/predict")
async def predict_route(text, max_length:int):
    try:
        conf = Configuration()
        obj = Prediction(conf.get_model_evaluation_config())
        text = obj.prediction(text, max_length=max_length)
        return text
    except Exception as e:
        raise e
    
if __name__ == "__main__":
    uvicorn.run(app, debug=True, host="127.0.0.1", port=8080)
