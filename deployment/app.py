# from fastapi import FastAPI

# # Creates our FastAPI application
# app = FastAPI()

# # Home route
# # returns JSON response of dictionary after the return statement
# @app.get("/")
# def home():
#     return {'data': 'Hello world'}

import onnxruntime as rt
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import nltk
import json
import numpy as np
import svc_model
from data_preprocessing import preprocess
def validate_port_number(input):
    while True:
        try:
            input = int(input)
        except:
            input = input("Enter valid Port Number: ")
        else:
            return input

app = FastAPI()

model = svc_model.load_model('./Modeling/SVC_model.pkl')

class Input(BaseModel):
    sentence: str


@app.post("/predict")
async def predict(text: Input, model=model):
    text_preprocessed = preprocess(text = str(text.sentence))

    result = svc_model.dialect_predict(model, text_preprocessed)

    text.sentence = result

    return text

port_number = validate_port_number(input("Enter Port Number: "))

uvicorn.run(app=app, host='127.0.0.1', port=port_number)