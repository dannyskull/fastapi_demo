from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import os
import io
import numpy as np
import cv2

yolo = FastAPI()

@yolo.post("/stream/")
async def upload(file: UploadFile = File(...)):
    filename = file.filename

    image_stream = io.BytesIO(file.file.read())

    image_stream.seek(0)
    
    file_bytes = np.array(bytearray(image_stream.read()),dtype=np.uint8)

    image  = cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)

    output_image  = image

    cv2.imwrite(f"results/{filename}",output_image)

    
    file_image = open(f"results/{filename}",mode="rb")

    return StreamingResponse(file_image,media_type="image/jpeg")
    