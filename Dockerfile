# Dockerfile
FROM python:3.10
COPY . /app
WORKDIR /app

ENV TZ=Europe/Moscow

RUN pip install -r requirements.txt


CMD ["python", "bot.py"]