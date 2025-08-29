FROM python:3.12-slim

ARG IP_ADDR
ARG PROFILE

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /lets_hack

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-traditional \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --index-url http://$IP_ADDR:8082/repository/pypi-all/simple/ --trusted-host $IP_ADDR:8082 -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["echo", "Use docker-compose to run the app"]
