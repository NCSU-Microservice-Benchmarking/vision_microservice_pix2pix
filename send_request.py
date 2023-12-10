#!/usr/bin/env python3
import requests

if __name__ == "__main__":
    host = "http://localhost:5000"
    # send a get request to the greet endpoint
    response = requests.get(host+"/greet")
    # print the response text
    print(response.text)
    # encode the images as binary strings 
    image = open("sample-image.png","rb").read()
    mask = open("sample-mask.png","rb").read()
    # put the image in a multipart form
    files = {"image":image,"mask":mask}
    # send a post request to the detect endpoint
    response = requests.post(host+"/",files=files)
    # check the response status code
    print(response.status_code)
    # save the image
    open("result.png","wb").write(response.content)
