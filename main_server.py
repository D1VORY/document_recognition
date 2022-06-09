import json
import os

from fastapi import FastAPI, File, UploadFile, Request, Form
import  aiofiles

from core.logic.recognizer import Recognizer

app = FastAPI()

@app.post("/recognize_yolo/")
async def recognize_yolo(file: UploadFile, template: str= Form(...)):
    try:
        json_data = json.loads(template)
    except json.decoder.JSONDecodeError:
        return {"message": "JSON ERROR"}
    filename = os.path.join(os.path.dirname(__file__), 'core', 'media', file.filename)
    async with aiofiles.open(filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    return Recognizer.recognize_yolo(json_data, filename)


@app.post("/recognize_vision_ai/")
async def recognize_vision_ai(file: UploadFile, template: str= Form(...)):
    try:
        json_data = json.loads(template)
    except json.decoder.JSONDecodeError:
        return {"message": "JSON ERROR"}
    filename = os.path.join(os.path.dirname(__file__), 'core', 'media', file.filename)
    async with aiofiles.open(filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    return Recognizer.recognize_visionai(json_data, filename)
