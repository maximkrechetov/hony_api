from fastapi import APIRouter, Depends, Response, HTTPException
from app.database import get_db
from app.schemas.auth import RegisterData
from app.models import Account
from sqlalchemy.orm import Session

router = APIRouter()

ACCOUNT_DEFAULT_TYPE_ID = 1


@router.post('/register')
async def register(data: RegisterData, db: Session = Depends(get_db)):
    """
    Register new user
    :param data: RegisterData instance
    :param db: db connection
    :return: new user data
    """
    account = db.query(Account).filter_by(phone=data.phone).first()

    if not account:
        account = Account(
            phone=data.phone,
            password=data.password,
            nickname=data.nickname,
            account_type_id=ACCOUNT_DEFAULT_TYPE_ID
        )

        db.add(account)
        db.commit()

        return Response(status_code=201)

    return HTTPException(status_code=409, detail="Account with given phone already exist")
