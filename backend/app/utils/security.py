"""
Security Utilities: Password Hashing & Standard Compliant JWT Tokens
"""
import os
import hmac
import hashlib
import json
import base64
import time
from typing import Optional, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.settings import settings
from app.exceptions.custom_exceptions import AuthenticationException


def _b64_url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64_url_decode(data_str: str) -> bytes:
    padding = "=" * (4 - len(data_str) % 4) if len(data_str) % 4 != 0 else ""
    return base64.urlsafe_b64decode(data_str + padding)


def hash_password(password: str) -> str:
    """Hash plaintext password using werkzeug security."""
    return generate_password_hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plaintext password against hash."""
    return check_password_hash(hashed_password, plain_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Create a signed JWT access token using standard library HMAC-SHA256."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    expire_minutes = expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire_time = int(time.time()) + (expire_minutes * 60)
    payload["exp"] = expire_time
    payload["iat"] = int(time.time())

    encoded_header = _b64_url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    encoded_payload = _b64_url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signature_base = f"{encoded_header}.{encoded_payload}".encode("utf-8")

    signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        signature_base,
        hashlib.sha256
    ).digest()
    encoded_signature = _b64_url_encode(signature)

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT access token."""
    try:
        parts = token.strip().split(".")
        if len(parts) != 3:
            raise AuthenticationException("Invalid token format.")

        encoded_header, encoded_payload, encoded_sig = parts
        signature_base = f"{encoded_header}.{encoded_payload}".encode("utf-8")
        expected_sig = hmac.new(
            settings.SECRET_KEY.encode("utf-8"),
            signature_base,
            hashlib.sha256
        ).digest()
        actual_sig = _b64_url_decode(encoded_sig)

        if not hmac.compare_digest(expected_sig, actual_sig):
            raise AuthenticationException("Invalid token signature.")

        payload_bytes = _b64_url_decode(encoded_payload)
        payload = json.loads(payload_bytes.decode("utf-8"))

        # Verify expiration
        exp = payload.get("exp")
        if exp and int(time.time()) > exp:
            raise AuthenticationException("Access token has expired. Please sign in again.")

        return payload
    except AuthenticationException:
        raise
    except Exception as e:
        raise AuthenticationException(f"Token validation failed: {str(e)}")
