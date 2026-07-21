# Intentionally old base image for container-scanner findings.
FROM python:3.9-slim-bullseye
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
COPY init.sql ./
RUN mkdir -p /app/data
EXPOSE 5001
CMD ["python", "app.py"]
