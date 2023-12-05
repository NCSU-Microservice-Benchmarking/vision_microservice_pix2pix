from flask import Flask, Response, request
from flask_cors import CORS
import numpy as np
import cv2

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Test with the following command:
# curl -F image=@sample-image.png -F mask=@sample-mask.png --output sample-output.png -X POST http://127.0.0.1:5000
@app.route('/',methods=['POST'])
def detect():
    if 'image' not in request.files or 'mask' not in request.files:
        return Response("invalid client input", status=400)
    image = request.files.get('image').read()
    mask = request.files.get('mask').read()
    try:
        return inpaint(image, mask)
    except:
        return Response("internal server error", status=500)

def inpaint(image: bytes, mask: bytes):
    # Process image
    result = image
    
    return Response(result, mimetype='image/png')
