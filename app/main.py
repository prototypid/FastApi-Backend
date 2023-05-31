from fastapi import FastAPI, status, HTTPException, Depends
from . import models, schemas
from typing import List
from sqlalchemy.orm import Session
from .database import engine, get_db


# create our models in the database
models.Base.metadata.create_all(bind=engine)



app = FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='blog',
#             user='postgres',
#             password='1324',
#             cursor_factory=RealDictCursor
#         )

#         cursor = conn.cursor()
#         print('Connected to database')
#         break
#     except Exception as e:
#         logging.error(e, exc_info=True)
#         time.sleep(10)


@app.get('/posts', response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/create_posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# def create_new_post(data: dict = Body()):
def create_new_post(data: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(**data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get('/posts/{post_id}', response_model=schemas.PostResponse)  
def get_post_with_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {post_id} was not found!'
        )

    return post


@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post_with_post_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post wit id {post_id} was not found!'
        )

    post.delete(synchronize_session=False)    
    db.commit()


@app.put('/posts/{post_id}', response_model=schemas.PostResponse)
def update_post_with_id(post_id: int, data: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {post_id} was not found!'
        )
    post_query.update(data.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()
