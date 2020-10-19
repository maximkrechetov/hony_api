from .default_model import DefaultModel
from sqlalchemy import Column, Integer, String, DateTime, func, orm
from sqlalchemy_utils import PasswordType
from app.database import db


class Account(DefaultModel):
    __tablename__ = 'account'

    phone = Column(String(16), nullable=False)
    nickname = Column(String(64), nullable=True)
    avatar = Column(String(128), nullable=True)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ))
    account_type_id = Column(Integer, ForeignKey('account_type.id'), index=True, nullable=False)
    account_active_to = Column(DateTime, nullable=True)

    account_type = orm.relation('AccountType')
