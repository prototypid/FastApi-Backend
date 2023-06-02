from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import schemas, models, database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = 'ab3a86bcb4c864d8a475d93d02be26bd647649c537dbfb06e807e8d6287a2d3f'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(payload: dict):
    data = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({'exp': expire})
    jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def verify_access_token(token, credential_exception):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = token_data.get('user_id')

        if id is None:
            raise credential_exception

        token_data = schemas.TokenData(id=user_id)

    except JWTError:
        raise credential_exception

    return token_data  # token_data == user_id


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    token_data = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user
