from app import schemas


# def test_get_all_users(client, test_user):
#     res = client.get('/users')
#     user = schemas.UserCreateResponse(res.json())


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
