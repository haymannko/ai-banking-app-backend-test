from fastapi import FastAPI, UploadFile, File
from ocr_model import OCR_Model

app = FastAPI(title="OCR Service API")


@app.post("/ocr/licence")
async def extract_licence(file: UploadFile = File(...)):
    """Extract NRC from licence image."""
    image_bytes = await file.read()
    ocr = OCR_Model(image_bytes=image_bytes)
    gray = ocr.preprocess_image_for_licence_ocr()
    nrc = ocr.licence_ocr_model(gray)
    return {"nrc": nrc or "Not found"}


@app.post("/ocr/passport")
async def extract_passport(file: UploadFile = File(...)):
    """Extract Passport number from passport image."""
    image_bytes = await file.read()
    ocr = OCR_Model(image_bytes=image_bytes)
    gray = ocr.preprocess_image_for_passport_ocr()
    passport_no = ocr.passport_ocr_model(gray)
    return {"passport": passport_no or "Not found"}
