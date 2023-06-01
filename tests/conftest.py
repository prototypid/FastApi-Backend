import logging
import pytest
from app import models
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1324@localhost/testblog'

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
def test_posts(session):

    posts_data = [{
        "title": "first title",
        "content": "first content",
    }, {
        "title": "2nd title",
        "content": "2nd content",
    },
        {
        "title": "3rd title",
        "content": "3rd content",
    }, {
        "title": "3rd title",
        "content": "3rd content",
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts


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
