import secrets
import uuid

ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate_uid(length: int = 32) -> str:
    """Generates a random id to be used as a uuid for any kind of relational operation.

    length is unused: a uuid4 hex string is always 32 characters.
    """
    return uuid.uuid4().hex


def generate_secure_uid(length: int = 32) -> str:
    """Generates a secure id that can be used for things like session ids."""
    return "".join(secrets.choice(ALLOWED_CHARS) for _ in range(length))
