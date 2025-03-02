from fastapi import APIRouter, Response, status, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.db import SessionDep
from app.models import User as UserModel
from app.schemas import User, TokenSchema
from app.auth import (
    get_hashed_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth")

@router.post('/token', summary="Auth2 Token Endpoint", response_model=TokenSchema, include_in_schema=False)
async def get_token(request: Request):
    access_token = request.cookies.get('access_token')

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token found",
        )

    return {"access_token": access_token, "token_type": "bearer"}



@router.post('/signup', summary="Create new user", response_model=User)
async def create_user(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user = session.query(UserModel).filter(UserModel.username == form_data.username).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )

    new_user = UserModel(
        username=form_data.username,
        password=get_hashed_password(form_data.password)
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return User(id=new_user.id, username=new_user.username, password=new_user.password)


@router.post('/login', summary="Create access token for user", include_in_schema=False)
async def login(response: Response, session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = session.query(UserModel).filter(UserModel.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=1800  # Token expiry in 30 minutes
    )

    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}


@router.get('/logout', summary="Logout user by clearing token", include_in_schema=False)
async def logout(response: Response):
    try:
        response.delete_cookie(key="access_token")
        return {"message": "Logout successful"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error logging out"
        )
