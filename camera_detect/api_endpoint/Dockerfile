FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libtesseract-dev \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --deploy --system

COPY . /app

EXPOSE 5006

CMD ["uvicorn", "cam_api:app", "--host", "0.0.0.0", "--port", "5006"]
