FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api/app.py ./app.py
COPY app/index.html /usr/share/nginx/html/index.html
COPY app/nginx.conf /etc/nginx/sites-available/default

EXPOSE 80

CMD ["sh", "-c", "gunicorn --bind 127.0.0.1:5000 app:app & nginx -g 'daemon off;'"]
