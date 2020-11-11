from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.schemas.auth import RegisterData, Token
from app.models import User
from app.auth import oauth2_scheme, create_access_token, authenticate_user, get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

USER_DEFAULT_TYPE_ID = 1


@router.post('/register')
async def register(data: RegisterData, db: Session = Depends(get_db)):
    """
    Register new user
    :param data: RegisterData instance
    :param db: db connection
    :return: 201 Created
    """
    user = db.query(User).filter_by(phone=data.phone).first()

    if not user:
        user = User(
            user_type_id=USER_DEFAULT_TYPE_ID,
            **data.dict()
        )

        db.add(user)
        db.commit()

        return Response(status_code=201)

    raise HTTPException(status_code=409, detail="User with given phone already exist")


@router.post("/auth_token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authentication.
    :param form_data: Form Data {login, password}
    :param db: db Session
    :return: Token object
    """
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.nickname})

    return {"access_token": access_token, "token_type": "bearer"}
