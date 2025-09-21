# AI Banking App Backend

A FastAPI-based backend application for AI-powered banking services, featuring OCR capabilities for document processing including license and passport recognition.

## Features

- **Document OCR Processing**: Extract text from license and passport images
- **FastAPI REST API**: High-performance async API endpoints
- **Error Monitoring**: Integrated Sentry for error tracking and monitoring
- **Image Preprocessing**: Advanced image enhancement for better OCR accuracy
- **Comprehensive Testing**: Unit tests for OCR functionality

## Tech Stack

- **Python**: 3.11.13
- **FastAPI**: Modern, fast web framework for building APIs
- **OpenCV**: Computer vision library for image processing
- **Tesseract OCR**: Optical character recognition engine
- **Sentry**: Error monitoring and performance tracking
- **Uvicorn**: ASGI server for FastAPI

## 📁 Project Structure

```
ai-banking-app-backend/
├── licence_ocr/
│   ├── api_endpoint/
│   │   ├── main.py          # FastAPI application and endpoints
│   │   └── ocr_model.py     # OCR model implementation
│   └── utils.py             # Utility functions and testing
├── tests/
│   └── test_ocr.py          # Unit tests for OCR functionality
├── Pipfile                  # Python dependencies
├── Pipfile.lock            # Locked dependency versions
└── README.md               # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-banking-app-backend/licence_ocr/api_endpoint
   ```

2. **Install dependencies using pipenv**
   ```bash
   pipenv install
   ```

3. **Activate the virtual environment**
   ```bash
   pipenv shell
   ```

4. **Install Tesseract OCR**
   - **macOS**: `brew install tesseract`
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

### Starting the API Server in *licence_ocr/api_endpoint* directory

```bash
uvicorn main:app --reload --port 5000
```

The server will start on `http://0.0.0.0:5000`

### API Endpoints

#### OCR Processing
- **POST** `/ocr`
  - **Description**: Process license or passport images for text extraction
  - **Parameters**:
    - `file`: Image file (UploadFile)
    - `class_name`: Document type - either "passport" or "licence" (Form)
  - **Response**: JSON with extracted text data

**Example Request:**
```bash
curl -X POST "http://localhost:5000/ocr" \
  -F "file=@path/to/your/image.jpg" \
  -F "class_name=licence"
```

**Example Response:**
```json
{
  "data": "12/ABC(N)1234567"
}
```

## Testing

Run the unit tests to verify OCR functionality:

```bash
python tests/test_ocr.py
```

## OCR Capabilities

### License OCR
- **Pattern Recognition**: Extracts NRC (National Registration Card) numbers
- **Format**: `DD/NAME(N)XXXXXXX` where:
  - `DD`: 1-2 digit day
  - `NAME`: Name in uppercase letters
  - `N`: Literal "N"
  - `XXXXXXX`: 5-7 digit/alphanumeric code
- **Preprocessing**: Brightness and contrast enhancement for better accuracy

### Passport OCR
- **Pattern Recognition**: Extracts passport numbers
- **Format**: `XX########` where:
  - `XX`: 1-2 uppercase letters
  - `########`: 6-8 digits
- **Preprocessing**: Grayscale conversion for optimal text recognition

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SENTRY_DSN=your_sentry_dsn_here
```

### Sentry Integration

The application includes Sentry integration for:
- Error tracking and monitoring
- Performance monitoring
- Transaction tracing for OCR operations


## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redoc`

