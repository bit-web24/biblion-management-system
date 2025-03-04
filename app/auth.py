import os
from typing import Union, Any, Optional
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from dotenv import load_dotenv
from passlib.context import CryptContext
from app.db import SessionDep
from app.models import User as UserModel
from app.schemas import User, TokenPayload

load_dotenv()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    expire = datetime.now(tz=timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)))
    )

    to_encode = {"exp": int(expire.timestamp()), "sub": str(subject)}
    secret_key = os.getenv("JWT_SECRET_KEY", "default_secret")
    algorithm = os.getenv("ALGORITHM", "HS256")

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


# OAuth2 Authentication scheme
reusable_oauth = OAuth2PasswordBearer(tokenUrl="/auth/token", scheme_name="JWT")


async def get_current_user(
    db: SessionDep, token: str = Depends(reusable_oauth)
) -> User:
    try:
        secret_key = os.getenv("JWT_SECRET_KEY", "default_secret")
        algorithm = os.getenv("ALGORITHM", "HS256")

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp, tz=timezone.utc) < datetime.now(
            tz=timezone.utc
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError) as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(UserModel).filter(UserModel.id == int(token_data.sub)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return User(id=user.id, username=user.username, password=user.password)
