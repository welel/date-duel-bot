FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    
WORKDIR /app

COPY requirements/ requirements/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements/base.txt \
    && rm -rf requirements

COPY . .

CMD ["python", "./src/bot.py"]
