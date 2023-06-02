from fastapi import APIRouter, status, HTTPException, Depends
from app import schemas, models, utils
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_new_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    pass_hashed = utils.hash_pass(user_data.password)
    user_data.password = pass_hashed
    new_user = models.User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{user_id}', response_model=schemas.UserCreateResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {user_id} does not exists!'
        )

    return user
