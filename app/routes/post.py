from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional
from app import schemas, models, oauth2


router = APIRouter(
    prefix='/posts',
    tags=['Post']
)


@router.get('/', response_model=List[schemas.PostResponse])
def get_all_posts(
        db: Session = Depends(get_db),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = ''
):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# def create_new_post(data: dict = Body()):
def create_new_post(
        data: schemas.PostCreate,
        db: Session = Depends(get_db),
        user=Depends(oauth2.get_current_user)
):
    post = models.Post(author_id=user.id, **data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get('/{post_id}', response_model=schemas.PostResponse)
def get_post_with_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {post_id} was not found!'
        )

    return post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post_with_post_id(
        post_id: int,
        db: Session = Depends(get_db),
        user=Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post wit id {post_id} was not found!'
        )

    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested actions.'
        )

    post_query.delete(synchronize_session=False)
    db.commit()


@router.put('/{post_id}', response_model=schemas.PostResponse)
def update_post_with_id(
        post_id: int,
        data: schemas.PostCreate,
        db: Session = Depends(get_db),
        user=Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {post_id} was not found!'
        )

    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action.'
        )
    post_query.update(data.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
