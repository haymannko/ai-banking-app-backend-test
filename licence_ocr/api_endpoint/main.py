from ocr_model import OCR_Model
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
import uvicorn
from contextlib import asynccontextmanager
import os 
import shutil
from typing import Literal

from prometheus_fastapi_instrumentator import Instrumentator


ocr_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the OCR model on startup and clean up on shutdown."""
    ocr_model_worker = OCR_Model()
    ocr_model['OCR_Model'] =  ocr_model_worker
    yield
    ocr_model.clear()

app = FastAPI(lifespan=lifespan)

@app.post("/ocr")
def ocr_endpoint(file: UploadFile = File(...), class_name: Literal['passport', 'licence'] = Form(...)
):
    """Endpoint to handle OCR requests."""
    try:
        temp_file = f"temp_{file.filename}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        ocr = ocr_model["OCR_Model"]
        ocr.image_path = temp_file

        if class_name == "passport":
            gray = ocr.preprocess_image_for_passport_ocr()
            result = ocr.passport_ocr_model(gray)

        elif class_name == "licence":
            gray = ocr.preprocess_image_for_licence_ocr()
            result = ocr.licence_ocr_model(gray)

        os.remove(temp_file)

        return {"data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.lifespan("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)