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
    text.sentence += ' Preprocessed'
    return text#{"predictions": outputs[0].tolist()}

port_number = validate_port_number(input("Enter Port Number: "))

uvicorn.run(app=app, host='127.0.0.1', port=port_number)