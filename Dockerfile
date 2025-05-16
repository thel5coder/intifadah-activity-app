FROM python:3.11-alpine

# Install dependencies
RUN apk update && apk add --no-cache \
    bash \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    curl \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

COPY . /app

EXPOSE 9000

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "intifadahactivity.wsgi:application"]