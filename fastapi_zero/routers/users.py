from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchemas,
)
from fastapi_zero.security import (
    get_current_user,
    get_password_hash,
)

app = APIRouter(prefix='/users', tags=['users'])


@app.post('/', status_code=201, response_model=UserPublic)
def create_users(user: UserSchemas, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/', response_model=UserList)
def read_users(limit: int = 10, offset: int = 0, session=Depends(get_session), current_user=Depends(get_current_user)):
    user = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': user}


@app.put('/{user_id}', response_model=UserPublic)
def update_user(
     user_id: int,
     user: UserSchemas,
     session=Depends(get_session),
     current_user=Depends(get_current_user)
    ):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions'
        )
    try:
        current_user.email = user.email
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exits'
        )


@app.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session=Depends(get_session),
    current_user=Depends(get_current_user)
    ):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions'
        )
    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted'}
