import os
from pathlib import Path
from dotenv import set_key, dotenv_values
import secrets

DEFAULT_ENV_FILE = Path('.env')

SECRET_VARS = [
    'SECRET_KEY',
    'OPENAI_API_KEY',
    'HUGGINGFACE_API_TOKEN',
    'GEMINI_API_KEY',
    'ANTHROPIC_API_KEY',
    'GOOGLE_CLIENT_SECRET',
    'GITHUB_CLIENT_SECRET',
]

def generate_value():
    return secrets.token_urlsafe(32)

def rotate_secrets(env_path=DEFAULT_ENV_FILE):
    env_path = Path(env_path)
    if not env_path.exists():
        print(f"Environment file {env_path} not found")
        return

    env_values = dotenv_values(env_path)
    for key in SECRET_VARS:
        new_val = generate_value()
        set_key(str(env_path), key, new_val)
        if key in env_values:
            print(f"Updated {key}")
        else:
            print(f"Added {key}")

if __name__ == '__main__':
    path = os.environ.get('ENV_FILE', str(DEFAULT_ENV_FILE))
    rotate_secrets(path)
