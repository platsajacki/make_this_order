FROM python:3.12

WORKDIR /app

COPY scr/requirements.txt .

RUN pip install -r scr/requirements.txt --no-cache-dir

COPY /src .

RUN python manage.py collectstatic --noinput
