import torch
import cv2 
from typing import Union,Annotated
from fastapi import FastAPI,File, UploadFile,Form
from fastapi.middleware.cors import CORSMiddleware
import json
from PIL import Image
import io
import base64
import urllib.parse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def lst2String(val):
    string = ""
    for i in val:
        string +=i
    return string

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/pt")
def read_root(username: Annotated[str, Form()]):
    """ if not username.startswith("file://"):
        raise ValueError("Invalid URI. It should start with 'file://'.")

    # Extract the file path from the URI
    file_path = urllib.parse.unquote(username[len("file://"):])
    image = Image.open(file_path) """
    return {"username": username}


#img = 'https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/zidane.jpg'


@app.get("/predict")
def read_root():  
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    url = 'https://th.bing.com/th/id/OIP.SlnjMSdNaDSG00NjiyOZEQHaFD?pid=ImgDet&rs=1'
    
    results = model(url)
    res = str(results)
    data_parts = res.split('\n')
    image_info = data_parts[0].split(': ')
    speed_info = data_parts[1].split(', ')
    result = {
    'image': image_info[0].strip(),
    'resolution': image_info[1].split()[0],
    'objects': image_info[1].split()[1:],
    'speed': {
        'pre-process': float(speed_info[0].split()[1].rstrip('ms')),
        'inference': float(speed_info[1].split()[0].rstrip('ms')),
        'NMS': float(speed_info[2].split()[0].rstrip('ms'))
    },
    'shape': speed_info[2].split()[5].strip('()').split(',')
    }
    json_data = json.dumps(result)
    print(json_data)
    return str(json_data)



@app.post("/upload-image")
async def upload_image(image: UploadFile = File(...)):
    #print("image")
    file_contents = await image.read()
    image_pil = Image.open(io.BytesIO(file_contents))
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    url = 'https://th.bing.com/th/id/OIP.SlnjMSdNaDSG00NjiyOZEQHaFD?pid=ImgDet&rs=1'
    #img = io.BytesIO(file_contents)
    results = model(image_pil)
    res = str(results)
    print(res)
    data_parts = res.split('\n')
    image_info = data_parts[0].split(': ')
    speed_info = data_parts[1].split(', ')
    result = {
    'image': image_info[0].strip(),
    'resolution': image_info[1].split()[0],
    'objects': image_info[1].split()[1:],
    'speed': {
        'pre-process': float(speed_info[0].split()[1].rstrip('ms')),
        'inference': float(speed_info[1].split()[0].rstrip('ms')),
        'NMS': float(speed_info[2].split()[0].rstrip('ms'))
    },
    'shape': speed_info[2].split()[5].strip('()').split(',')
    }
    json_data = json.dumps(result)
    """ val = json_data["objects"]
    predicted_objs= lst2String(val) """
    print(json_data)
    data_dict = json.loads(json_data)
    print(data_dict["objects"])
    val = data_dict["objects"]
    predicted_objs= lst2String(val)
    print(predicted_objs)
    # Display the image
    #image_pil.show()
    return predicted_objs



@app.post("/files/")
async def create_file(image:Annotated[bytes,File()]):
    #print(image)
    img = str(image)
    #file_contents = await image.read()Annotated[bytes,File()]
    base64_image_data = img.split(",")[1]
    #print(base64_image_data)
    
    # Decode the base64 image data
    decoded_image_data = base64.b64decode(base64_image_data)
    image_pil = Image.open(io.BytesIO(decoded_image_data))
    #image_pil.show()
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    url = 'https://th.bing.com/th/id/OIP.SlnjMSdNaDSG00NjiyOZEQHaFD?pid=ImgDet&rs=1'
    #img = io.BytesIO(image_pil)
    results = model(image_pil)
    res = str(results)
    data_parts = res.split('\n')
    image_info = data_parts[0].split(': ')
    speed_info = data_parts[1].split(', ')
    result = {
    'image': image_info[0].strip(),
    'resolution': image_info[1].split()[0],
    'objects': image_info[1].split()[1:],
    'speed': {
        'pre-process': float(speed_info[0].split()[1].rstrip('ms')),
        'inference': float(speed_info[1].split()[0].rstrip('ms')),
        'NMS': float(speed_info[2].split()[0].rstrip('ms'))
    },
    'shape': speed_info[2].split()[5].strip('()').split(',')
    }
    json_data = json.dumps(result)
    """ val = json_data["objects"]
    predicted_objs= lst2String(val) """
    print(json_data)
    data_dict = json.loads(json_data)
    print(data_dict["objects"])
    val = data_dict["objects"]
    predicted_objs= lst2String(val)
    print(res)
    print(predicted_objs)
    #return {"file_size":len(image)}
    return predicted_objs

@app.post("/file")
async def create_file(image: UploadFile):
    #base64_image_data = image.split(",")[1]
    
    # Decode the base64 image data
    #decoded_image_data = base64.b64decode(base64_image_data)
    
    return {"file_size":len(image)}


@app.post("/send")
async def create_file(image:Annotated[bytes,File()]):
    img = str(image)

    return {"file_size":len(image)}