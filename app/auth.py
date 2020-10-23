from os import environ
from typing import Optional
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from .models import User
from .database import get_db
from sqlalchemy.orm import Session


SECRET_KEY = environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(
    schemes=[
        'pbkdf2_sha512',
        'md5_crypt'
    ],
    deprecated=['md5_crypt']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth_token")


def verify_password(form_password, db_password):
    return pwd_context.verify(form_password, db_password.hash)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    return db.query(User).filter_by(nickname=username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(db, username)

    if user is None:
        raise credentials_exception

    return user
