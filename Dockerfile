FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD gunicorn --worker-class gevent \
  --workers 3 \
  --bind 0.0.0.0:80 \
  --worker-connections 10 \
  --timeout 30 \
  --limit-request-line 0 \
  --preload \
  patched:app
