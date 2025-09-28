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



import grpc
from concurrent import futures
import ocr_pb2, ocr_pb2_grpc
from ocr_model import OCR_Model


class NrcOcrService(ocr_pb2_grpc.nrc_ocr_serviceServicer):
    def AddLicenceOCR(self, request, context):
        ocr = OCR_Model(image_bytes=request.licence)
        gray = ocr.preprocess_image_for_licence_ocr()
        nrc = ocr.licence_ocr_model(gray)
        return ocr_pb2.AddOutputNRC(output_nrc=nrc or "")

    def AddLicencePassport(self, request, context):
        ocr = OCR_Model(image_bytes=request.passport)
        gray = ocr.preprocess_image_for_passport_ocr()
        passport_no = ocr.passport_ocr_model(gray)
        return ocr_pb2.AddOutputNRC(output_nrc=passport_no or "")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ocr_pb2_grpc.add_nrc_ocr_serviceServicer_to_server(NrcOcrService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
