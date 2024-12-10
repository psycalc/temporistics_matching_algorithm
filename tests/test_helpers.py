import uuid

def unique_username(prefix="testuser"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def unique_email(prefix="test", domain="example.com"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@{domain}"
