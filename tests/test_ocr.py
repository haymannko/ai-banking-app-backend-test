import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from licence_ocr.api_endpoint.ocr_model import OCR_Model

class TestLicenceOCR(unittest.TestCase):
    def setUp(self):
        self.ocr_model = OCR_Model("test.jpg")

    def test_preprocess_image_for_licence_ocr(self):
        gray_img = self.ocr_model.preprocess_image_for_licence_ocr()
        self.assertIsNotNone(gray_img)
        self.assertEqual(len(gray_img.shape), 2)  # Check if the image is grayscale

    def test_licence_ocr_model(self):
        gray_img = self.ocr_model.preprocess_image_for_licence_ocr()
        nrc = self.ocr_model.licence_ocr_model(gray_img)
        self.assertIsInstance(nrc, str)
        self.assertRegex(nrc, r'\d{1,2}/[A-Z ]+\(N\)[0-9O]{5,7}')

class TestPassportOCR(unittest.TestCase):
    def setUp(self):
        self.ocr_model = OCR_Model("test1.jpeg")

    def test_preprocess_image_for_passport_ocr(self):
        gray_img = self.ocr_model.preprocess_image_for_passport_ocr()
        self.assertIsNotNone(gray_img)
        self.assertEqual(len(gray_img.shape), 2)  # Check if the image is grayscale

    def test_passport_ocr_model(self):
        gray_img = self.ocr_model.preprocess_image_for_passport_ocr()
        passport_number = self.ocr_model.passport_ocr_model(gray_img)
        self.assertIsInstance(passport_number, str)
        self.assertRegex(passport_number, r"\b[A-Z]{1,2}[0-9]{6,8}\b")

if __name__ == '__main__':
    unittest.main()