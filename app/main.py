from fastapi import FastAPI
from . import models
from .database import engine
from .routes import user, post, auth
from fastapi.middleware.cors import CORSMiddleware


# create our models in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
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
