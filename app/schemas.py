from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):

    title: str
    post: str
    publish: bool = True
    rating: Optional[int] = None