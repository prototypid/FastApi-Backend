import pytest
from app import schemas
from jose import jwt


# def test_get_all_users(client, test_user):
#     res = client.get('/users')
#     user = schemas.UserCreateResponse(res.json())
SECRET_KEY = 'ab3a86bcb4c864d8a475d93d02be26bd647649c537dbfb06e807e8d6287a2d3f'


def test_create_user(client):
    user_details = {
        'email': 'mee@example.com',
        'password': 'password1234'
    }

    res = client.post('/users', json=user_details)
    user = schemas.UserCreateResponse(**res.json())

    assert user.email == user_details['email']
    assert res.status_code == 201


def test_get_user_with_id(client, test_user):
    res = client.get(f'/users/{test_user["id"]}')
    print(res.json())
    user = schemas.UserCreateResponse(**res.json())
    assert user.id == test_user['id']
    assert user.email == test_user['email']


def test_user_login(client, test_user):
    res = client.post(
        '/login',
        data={'username': test_user['email'], 'password': test_user['password']}
    )
    res_data = schemas.Token(**res.json())
    token_data = jwt.decode(res_data.access_token, SECRET_KEY, algorithms='HS256')
    assert res.status_code == 200
    assert res_data.token_type == 'bearer'
    assert token_data.get('id') == test_user.get('user_id')


@pytest.mark.parametrize(
    'email, password, status',
    [
        ('me@mail.com', '1234', 403),
        ('next@mail.com', 'nothing', 403),
        (None, 'something', 422),
        ('something@mail.com', None, 422),
        (None, None, 422),
        ('some', '1234', 403)
    ]
)
def test_incorrect_login(client, email, password, status):
    res = client.post('/login', data={'username': email, 'password': password})

    assert res.status_code == status
