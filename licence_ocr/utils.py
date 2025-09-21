"""
OCR Model calls
"""

from api_endpoint.ocr_model import OCR_Model

ocr = OCR_Model(image_path="f28c917b-7483-4249-b761-1ec60101f9c8.jpeg")

# preprocess_image_for_ocr = ocr.preprocess_image_for_licence_ocr(image_path="IMG_6805.jpg")
# nrc = ocr.licence_ocr_model(preprocess_image_for_ocr)
# print("NRC:", nrc)

preprocess_image_for_ocr_passport = ocr.preprocess_image_for_passport_ocr()
nrc = ocr.passport_ocr_model(preprocess_image_for_ocr_passport)
print("Passport:", nrc)
