from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from .schemas import Post

app = FastAPI()


@app.get('/posts')
def get_all_posts():
    return {'data': 'There is no post currently.'}


@app.post('/create_posts')
# def create_new_post(data: dict = Body()):
def create_new_post(data: Post):
    print(data)
    return {'message': 'Successfully recieved your request.'}


@app.get('/posts/{post_id}')  
def get_post_with_id(post_id: int, response: Response):
    post = None
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {post_id} was not found!'
        )

        return {'message': f'Post with id {post_id} was not found!'}
    return {'message': 'Post'}