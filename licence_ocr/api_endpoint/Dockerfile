FROM python:3.11-slim

ENV PORT=5001
EXPOSE $PORT

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

RUN pip install pydantic-core

COPY ./licence_ocr/api_endpoint /app

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]