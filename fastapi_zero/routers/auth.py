from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.security import (
    create_access_token,
    verify_password,
)

app = APIRouter(prefix='/auth', tags=['auth'])


@app.post('/token')
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session=Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    if not verify_password(form_data.password, user.passwrod):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
        acess_token = create_access_token({'sub': user.email})
        return {'acess_token': acess_token, 'token_type': 'Bearer'}
