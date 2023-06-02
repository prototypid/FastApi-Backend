from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models, utils, oauth2
from app.database import get_db

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def user_login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid credentials'
        )

    if not utils.verify_pass(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )

    token = oauth2.create_access_token({'user_id': user.id})
    return {'access_token': token, 'token_type': 'bearer'}
