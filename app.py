from flask import Flask, Response, request
from flask_cors import CORS
from person_remover.pix2pix.utils.model import Pix2Pix
import numpy as np
import tensorflow as tf

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/greet')
def greet():
    return("Hello")

# Quickly test with the following command:
# curl -F image=@sample-image.png -F mask=@sample-mask.png --output result.png -X POST http://127.0.0.1:5000
@app.route('/',methods=['POST'])
def inpaint():
    if 'image' not in request.files or 'mask' not in request.files:
        return Response("invalid client input", status=400)
    image = request.files.get('image').read()
    mask = request.files.get('mask').read()
    try:
        return inpaint(image, mask)
    except Exception as e:
        return Response("internal server error", status=500)

def inpaint(image: bytes, mask: bytes):
    # TODO Push model after it finishes training...
    
    result = image
        
    return Response(result, mimetype='image/png')
