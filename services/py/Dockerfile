FROM python:3.13-slim

WORKDIR /app

COPY services/py/requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY services/py/ /app/

RUN useradd -m reverseproxy
USER reverseproxy

ENV PYTHONPATH=/app/

CMD ["python", "main.py"]