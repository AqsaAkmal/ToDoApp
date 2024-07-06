# frontend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY ./app /app

RUN pip install -r /app/requirements.txt

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
