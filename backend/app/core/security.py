import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
import bcrypt
import jwt

from app.core.config import settings

logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the stored bcrypt hash.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False


def get_password_hash(password: str) -> str:
    """
    Generate a bcrypt hash for a plain password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
    role: Optional[str] = None
) -> str:
    """
    Generate a signed JWT access token with an expiration time and optional role claim.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    if role:
        to_encode["role"] = str(role)

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.
    Returns the token payload if valid, None otherwise.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        logger.warning(f"JWT decode error: {e}")
        return None
