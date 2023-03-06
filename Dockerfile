FROM python

WORKDIR /app
COPY src/* /app
COPY requirements/* /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]