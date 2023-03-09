FROM python:3.10-alpine

WORKDIR /app

COPY requirements/* /app
RUN pip install -r requirements.txt

COPY src/* /app

ENTRYPOINT ["python"]
CMD ["app.py"]