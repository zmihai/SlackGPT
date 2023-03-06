FROM python:3.10-alpine

WORKDIR /app
COPY src/* /app
COPY requirements/* /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]