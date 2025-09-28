# AI Banking App Backend

A FastAPI-based backend application for AI-powered banking services, featuring OCR capabilities for document processing including license and passport recognition.

## 🚀 Features

- **Document OCR Processing**: Extract text from license and passport images
- **FastAPI REST API**: High-performance async API endpoints
- **Error Monitoring**: Integrated Sentry for error tracking and monitoring
- **Image Preprocessing**: Advanced image enhancement for better OCR accuracy
- **Docker Support**: Containerized deployment with Docker

## 🛠️ Tech Stack

- **Python**: 3.11.13
- **FastAPI**: Modern, fast web framework for building APIs
- **OpenCV**: Computer vision library for image processing
- **Tesseract OCR**: Optical character recognition engine
- **Sentry**: Error monitoring and performance tracking
- **Uvicorn**: ASGI server for FastAPI
- **Docker**: Containerization platform

## 📁 Project Structure

```
ai-banking-app-backend/
├── licence_ocr/
│   ├── api_endpoint/
│   │   ├── main.py          # FastAPI application and endpoints
│   │   ├── ocr_model.py     # OCR model implementation
│   │   └── Dockerfile       # Docker configuration
│   └── utils.py             # Utility functions and testing
├── tests/
│   └── test_ocr.py          # Unit tests for OCR functionality
├── Pipfile                  # Python dependencies
├── Pipfile.lock            # Locked dependency versions
└── README.md               # This file
```

## 🐳 Docker Deployment

### Prerequisites
- Docker installed on your system
- Git (to clone the repository)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-banking-app-backend
   ```

2. **Build the Docker image**
   ```bash
   docker build -f licence_ocr/api_endpoint/Dockerfile -t ocr-api .
   ```

3. **Run the container**
   ```bash
   docker run -p 5000:5000 -e SENTRY_DSN=your_sentry_dsn ocr-api
   ```

4. **Access the API**
   - API: `http://localhost:5000`
   - Documentation: `http://localhost:5000/docs`

### Docker Environment Variables

Create a `.env` file in the project root:
```env
SENTRY_DSN=your_sentry_dsn_here
```

Run with environment file:
```bash
docker run -p 5000:5000 --env-file .env ocr-api
```

### Docker Compose (Alternative)

Create a `docker-compose.yml` in the project root:
```yaml
version: '3.8'

services:
  ocr-api:
    build:
      context: .
      dockerfile: licence_ocr/api_endpoint/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - SENTRY_DSN=${SENTRY_DSN:-}
    restart: unless-stopped
```

Run with Docker Compose:
```bash
docker-compose up --build
```

### Docker Build Options

**Development Build:**
```bash
docker build -f licence_ocr/api_endpoint/Dockerfile -t ocr-api:dev .
```

**Production Build:**
```bash
docker build -f licence_ocr/api_endpoint/Dockerfile -t ocr-api:prod --target production .
```

**Build with No Cache:**
```bash
docker build --no-cache -f licence_ocr/api_endpoint/Dockerfile -t ocr-api .
```

### Docker Container Management

**View running containers:**
```bash
docker ps
```

**View container logs:**
```bash
docker logs <container_id>
```

**Stop container:**
```bash
docker stop <container_id>
```

**Remove container:**
```bash
docker rm <container_id>
```

**Remove image:**
```bash
docker rmi ocr-api
```

## 🔧 Local Development

### Installation

1. **Install dependencies using pipenv**
   ```bash
   pipenv install
   ```

2. **Activate the virtual environment**
   ```bash
   pipenv shell
   ```

3. **Install Tesseract OCR**
   - **macOS**: `brew install tesseract`
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Running Locally

```bash
python licence_ocr/api_endpoint/main.py
```

## 📋 API Endpoints

### OCR Processing
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

## 🧪 Testing

Run the unit tests:
```bash
python -m pytest tests/test_ocr.py -v
```

## 📝 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.