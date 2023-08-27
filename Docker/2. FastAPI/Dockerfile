
FROM python:3.11.4

WORKDIR /fast-api

COPY requirements.txt .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]
