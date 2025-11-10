import json
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import StreamingResponse
import cv2
import io
app = FastAPI()

items = []

@app.get("/")
def root():
    return {"message": "Meeeeh"}

@app.get('/image', response_class=StreamingResponse)
def get_image():
    img = cv2.imread("sheep.jpg")
    buf = cv2.imencode('.png', img)[1].tobytes()
    return StreamingResponse(io.BytesIO(buf), media_type="image/png")