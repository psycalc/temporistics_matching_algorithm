# Helper script to ensure the PostgreSQL container is running

#!/usr/bin/env python3
import subprocess
import sys
import time


def container_running():
    result = subprocess.run([
        "docker", "ps", "--filter", "name=postgres", "--format", "{{.Names}}"
    ], stdout=subprocess.PIPE, text=True)
    return bool(result.stdout.strip())


def start_container():
    subprocess.run(["docker-compose", "up", "-d", "db"], check=True)


def wait_for_connection(max_attempts=10, delay=2):
    attempts = 0
    while attempts < max_attempts:
        result = subprocess.run(
            ["docker-compose", "exec", "db", "psql", "-U", "testuser", "-d", "testdb", "-c", "SELECT 1"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return True
        attempts += 1
        time.sleep(delay)
    return False


def get_container_ip():
    result = subprocess.run([
        "docker", "inspect", "-f",
        "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
        "temporistics_matching_algorithm-db-1"
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    return result.stdout.strip()


def main():
    if not container_running():
        print("Starting PostgreSQL container...", file=sys.stderr)
        start_container()
    if not wait_for_connection():
        print("Failed to connect to PostgreSQL", file=sys.stderr)
        sys.exit(1)
    host = get_container_ip() or "localhost"
    print(host)


if __name__ == "__main__":
    main()
