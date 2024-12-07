# Stage 1: Build dependencies
FROM python:3.8-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libc6-dev
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Copy the dependencies and application code
FROM python:3.8-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .

# Copy entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN ls -l /entrypoint.sh && cat /entrypoint.sh

EXPOSE 5000
ENV FLASK_APP run.py
ENV FLASK_ENV production

ENTRYPOINT ["/bin/sh"]
CMD ["-c", "echo 'Container started' && exec pytest"]
