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
from test_results import predict_ounx

def indexs(x, word2ind):
    arr = np.empty(len(x))
    i = 0
    for word in x:
        id = word2ind[word]
        arr[i] = id
        i+=1
    return arr

def preaction(text):
       # Tokenize the text into a list of words
        text = nltk.word_tokenize(text)
        with open('deployment\word2ind.txt', 'r') as file:
            word2ind = json.load(file)
        text = indexs(text, word2ind)
        x_test_padded = np.zeros( 24,)
        x_test_padded[:len(text)] = text


        x_test_padded = np.array(x_test_padded,dtype= np.float32)

        return x_test_padded

def validate_port_number(input):
    while True:
        try:
            input = int(input)
        except:
            input = input("Enter valid Port Number: ")
        else:
            return input

app = FastAPI()
# session = rt.InferenceSession("model.onnx")  # Replace "model.onnx" with the path to your ONNX model
class Item(BaseModel):
    sentence: str

@app.post("/predict")
async def predict(text: Item):
    # preprocessed_text = preprocess(text)
    # inputs = encode(preprocessed_text)
    # outputs = session.run(None, {"input": inputs})
    result = preaction(str(text.sentence))
    result = predict_ounx("deployment\model3.onnx",result.reshape(1,-1))
    # print(result)
    # text.sentence+= 'ddd'
    text.sentence = result
    print(result)
    return text#{"predictions": outputs[0].tolist()}

port_number = validate_port_number(input("Enter Port Number: "))

uvicorn.run(app=app, host='127.0.0.1', port=port_number)