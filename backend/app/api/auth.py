from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.api.deps import get_current_user, get_user_response

router = APIRouter()


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new learner account.
    Returns access token and user profile upon successful registration.
    """
    # Normalize email to lowercase
    normalized_email = user_in.email.strip().lower()

    existing_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    # Create new user (Public registration ALWAYS enforces STUDENT role)
    hashed_pwd = get_password_hash(user_in.password)
    new_user = User(
        name=user_in.name.strip(),
        email=normalized_email,
        password_hash=hashed_pwd,
        role="STUDENT",
        diagnostic_completed=False,
        diagnostic_exempt=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    access_token = create_access_token(subject=new_user.id, role=new_user.role)
    user_response = get_user_response(new_user)

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="User login"
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with email and password.
    Returns JWT access token and user details.
    """
    normalized_email = credentials.email.strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id, role=user.role)
    user_response = get_user_response(user)

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile"
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Fetch the currently authenticated user profile and onboarding status.
    """
    return get_user_response(current_user)
