from keras.models import load_model
import numpy as np
import onnxruntime as ort
import onnx
from convert_onnx  import shapes 

def comparsion(path_tf,path_onnx, input_data):

    model = load_model(path_tf)
    results_tf = model.predict(input_data)
    
    sess = ort.InferenceSession(path_onnx, providers=["CUDAExecutionProvider"])
    
    input_ounx_shape, output_ounx_shape = shapes(path_onnx)

    results_ort = sess.run([f"{output_ounx_shape}"], {f"{input_ounx_shape}": input_data})
    results_ort = np.array(results_ort).reshape(1,1)
    
    for ort_res, tf_res in zip(results_ort, results_tf):
        np.testing.assert_allclose(ort_res, tf_res, rtol=1e-5, atol=1e-5)
        
    print("Results match")
    return 1

def predict_ounx(path_onnx, input_data):
    sess = ort.InferenceSession(path_onnx, providers=["CUDAExecutionProvider"])
    
    input_ounx_shape, output_ounx_shape = shapes(path_onnx)

    results_ort = sess.run([f"{output_ounx_shape}"], {f"{input_ounx_shape}": input_data})
    results_ort = np.array(results_ort).reshape(1,1)

    return 'Positive' if results_ort >= 0.5 else 'Negative'







