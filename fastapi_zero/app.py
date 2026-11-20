from http import HTTPStatus

from fastapi import  FastAPI, HTTPException

from fastapi_zero.schemas import Message
from fastapi_zero.routers import auth,users

app = FastAPI()

app.include_router(auth.app)
app.include_router(users.app)

@app.get('/', status_code=200)
def read_root():
    return {'message': 'Ola mundo'}

