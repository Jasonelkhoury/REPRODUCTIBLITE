
FROM python:3.14-slim

WORKDIR /app

COPY tp1.py /app/tp1.py

CMD ["python", "tp1.py"]
