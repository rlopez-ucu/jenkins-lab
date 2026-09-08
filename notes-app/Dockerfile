FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir flask==3.0.3

COPY notes.py app.py ./

ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION

EXPOSE 5000
CMD ["python", "app.py"]
