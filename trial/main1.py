from typing import Union
from fastapi import FastAPI, File, UploadFile
import torch
import json
from random import randint
import uuid
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's URL or "*" to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict the HTTP methods as needed
    allow_headers=["*"],  # You can restrict the headers as needed
)
IMAGEDIR = "images/"

@app.get("/")
def read_root():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    img = 'https://live.staticflickr.com/65535/49362146333_1a47a9a927_b.jpg'
    results = model(img)
    print(results)
    print(type(results))
    res = str(results)
    return res


@app.post("/")
def get_image():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    img = 'https://live.staticflickr.com/65535/49362146333_1a47a9a927_b.jpg'
    results = model(img)
    print(results)
    print(type(results))
    res = str(results)
    return res

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
 
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
 
    #save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
 
    return {"filename": file.filename}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post("/upload_image")
async def upload_image(file: UploadFile):
    contents = await file.read() 
    # Return a response indicating successful upload along with the file name
    return {"message": "Image uploaded successfully.", "filename": file.filename}
