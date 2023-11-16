FROM python:3.9-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install psycopg2-binary

EXPOSE 8000

RUN chmod +x /app/app-entrypoint.sh
