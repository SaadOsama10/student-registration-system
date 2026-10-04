"""Password hashing with PBKDF2-HMAC-SHA256 (standard library only).

Stored format: pbkdf2_sha256$<iterations>$<salt hex>$<hash hex>
"""
import hashlib
import hmac
import secrets

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"{ALGORITHM}${ITERATIONS}${salt.hex()}${digest.hex()}"


def is_hashed(stored: str) -> bool:
    return isinstance(stored, str) and stored.startswith(ALGORITHM + "$")


def verify_password(password: str, stored: str) -> bool:
    """Check a password against a stored hash.

    Plain-text values from databases created before hashing was added are
    still accepted, so callers can upgrade them with hash_password().
    """
    if not stored:
        return False
    if not is_hashed(stored):
        return hmac.compare_digest(password.encode("utf-8"), str(stored).encode("utf-8"))
    try:
        _, iterations, salt_hex, hash_hex = stored.split("$")
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(digest.hex(), hash_hex)
