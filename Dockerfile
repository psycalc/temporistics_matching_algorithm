# Stage 1: Build dependencies
FROM python:3.8-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libc6-dev libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Copy the dependencies and application code
FROM python:3.8-slim
WORKDIR /app

# Устанавливаем postgresql-client для pg_isready
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local
COPY . .

# Copy entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port and set environment variables
EXPOSE 5000
ENV FLASK_APP run.py
ENV FLASK_ENV production

ENTRYPOINT ["/entrypoint.sh"]
