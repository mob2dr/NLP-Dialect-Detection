from keras.models import load_model
import tf2onnx
import onnx
import tensorflow as tf


def converter (path_model, path_output_model):
 

    
    model = load_model(path_model)
   


    # Use from_function for tf functions
    input_signature = [tf.TensorSpec((None, None), tf.float32, name='input')]
    onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature ,opset=13)
    output_model = f'{path_output_model}'+'.onnx'
    onnx.save(onnx_model, output_model)
    
def shapes(path_mode_onnx):

    mode_onnx = onnx.load(path_mode_onnx)
    for input in mode_onnx.graph.input:
       inputs  = input.name

  
    for output in mode_onnx.graph.output:
       outputs = output.name
    
    return inputs, outputs





