from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import user_repository
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

def register_user(db: Session, user_in: UserCreate):
    existing = user_repository.get_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed = hash_password(user_in.password)
    return user_repository.create_user(db, user_in, hashed)

def authenticate_user(db: Session, email: str, password: str):
    user = user_repository.get_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return token