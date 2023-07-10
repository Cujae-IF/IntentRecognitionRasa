FROM python:3.10.6-alpine3.14

WORKDIR /app

COPY requirements.txt .

RUN pip install requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]