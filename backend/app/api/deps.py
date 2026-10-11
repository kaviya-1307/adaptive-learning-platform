from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.schemas.user import UserResponse

# HTTP Bearer token scheme
security_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to authenticate and retrieve the current user from JWT token.
    Raises 401 Unauthorized if token is missing, invalid, or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id_str: Optional[str] = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional user auth dependency. Returns User if valid token provided, else None.
    """
    if not credentials or not credentials.credentials:
        return None

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        return None

    user_id_str: Optional[str] = payload.get("sub")
    if user_id_str is None:
        return None

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        return None

    return db.query(User).filter(User.id == user_id).first()


def get_user_response(user: User) -> UserResponse:
    """
    Helper to convert a User model instance to UserResponse schema
    with onboarding status, role, and diagnostic completion state populated.
    """
    has_onboarded = user.onboarding_profile is not None
    goal = user.onboarding_profile.learning_goal if has_onboarded else None
    exp = user.onboarding_profile.experience_level if has_onboarded else None
    user_role = getattr(user, "role", "STUDENT") or "STUDENT"
    diag_completed = getattr(user, "diagnostic_completed", False) or False
    diag_exempt = getattr(user, "diagnostic_exempt", False) or False
    diag_score = getattr(user, "diagnostic_score", None)
    diag_total = getattr(user, "diagnostic_total", None)
    diag_completed_at = getattr(user, "diagnostic_completed_at", None)

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user_role,
        created_at=user.created_at,
        onboarding_completed=has_onboarded,
        learning_goal=goal,
        experience_level=exp,
        diagnostic_completed=diag_completed,
        diagnostic_exempt=diag_exempt,
        diagnostic_score=diag_score,
        diagnostic_total=diag_total,
        diagnostic_completed_at=diag_completed_at
    )


def require_diagnostic_completed(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Authorization dependency ensuring the user has completed the required diagnostic assessment
    before accessing normal learning and recommendation features.
    Existing legacy users and administrators are exempt.
    """
    role = getattr(current_user, "role", "STUDENT") or "STUDENT"
    if role == "ADMIN":
        return current_user
    if getattr(current_user, "diagnostic_exempt", False):
        return current_user
    if getattr(current_user, "diagnostic_completed", False):
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Diagnostic assessment required before accessing learning features."
    )


def require_student(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Authorization dependency ensuring the user can access student functionality.
    Both STUDENT and ADMIN can access standard student/learning workflows.
    """
    role = getattr(current_user, "role", "STUDENT") or "STUDENT"
    if role not in ("STUDENT", "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student or Admin access required."
        )
    return current_user


def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Authorization dependency ensuring the user has ADMIN privileges.
    Raises 403 Forbidden for STUDENT or any non-admin role.
    """
    role = getattr(current_user, "role", "STUDENT") or "STUDENT"
    if role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required."
        )
    return current_user
