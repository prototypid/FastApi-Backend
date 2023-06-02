import logging
import pytest
from app import models, oauth2
from app.main import app
from app.config import settings
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@' \
                          f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1324@localhost/testblog'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_details = {
        'email': 'me@example.com',
        'password': 'password1234'
    }

    try:
        res = client.post('/users', json=user_details)

        assert res.status_code == 201
    except AssertionError as e:
        logging.error(e)
        logging.error('User was not created')
        pass
    else:
        user = res.json()
        user['password'] = user_details['password']
        return user


@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }

    return client


@pytest.fixture
def test_posts(session, test_user):

    posts_data = [{
        "title": "first title",
        "content": "first content",
        "author_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "author_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "author_id": test_user['id']
        }, {
        "title": "3rd title",
        "content": "3rd content",
        "author_id": test_user['id']

        }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']),
    #                 models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
