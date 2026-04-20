FROM python:3.10.8-slim
LABEL maintainer="hbaklanova@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

USER my_user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
