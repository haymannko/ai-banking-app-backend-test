import cv2 
import pytesseract
import re 
import numpy as np

class OCR_Model:
    """OCR Model for extracting NRC and Passport from images."""

    def __init__(self, image_path: str = None, image_bytes: bytes = None):
        self.image_path = image_path 
        self.image_bytes = image_bytes

    def load_image(self):
        """Load image from path or bytes."""
        if self.image_path:
            return cv2.imread(self.image_path)
        if self.image_bytes:
            nparr = np.frombuffer(self.image_bytes, np.uint8)
            return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        raise ValueError("No image source provided.")

    def preprocess_image_for_licence_ocr(self):
        image = self.load_image()
        brightness = 10
        contrast = 2
        image2 = cv2.addWeighted(
            image, contrast, np.zeros(image.shape, image.dtype), 0, brightness
        )
        gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        return gray

    def licence_ocr_model(self, gray_img):
        result = pytesseract.image_to_string(gray_img)
        pattern = re.compile(r"\d{1,2}/[A-Z ]+\(N\)[0-9O]{5,7}", re.IGNORECASE)
        match = pattern.search(result)
        if match:
            nrc = match.group()
            clean_nrc = re.sub(r"O", "0", nrc)  # O → 0
            clean_nrc = re.sub(r" ", "", clean_nrc)
            return clean_nrc
        return None

    def preprocess_image_for_passport_ocr(self):
        image = self.load_image()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    def passport_ocr_model(self, gray_img):
        result = pytesseract.image_to_string(gray_img)
        pattern = r"\b[A-Z]{1,2}[0-9]{6,8}\b"
        matches = re.findall(pattern, result)
        return matches[0] if matches else None

