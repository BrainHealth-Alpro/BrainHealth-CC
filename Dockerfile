FROM python:3.10.14

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    libffi-dev \
    libssl-dev \
    libgl1-mesa-glx \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN cp .env.example .env && \
    SECRET_KEY=$(python3 -c "import os; print(os.urandom(24).hex())") && \
    sed -i "s/^FLASK_SECRET_KEY=.*$/FLASK_SECRET_KEY=${SECRET_KEY}/" .env

EXPOSE 5000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
