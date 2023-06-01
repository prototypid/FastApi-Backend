import pytest
from app import schemas


def test_get_all_posts(client, test_posts):
    res = client.get('/posts')
    print()
    print(type(res.json()), res.json())
    def validate(post):
        return schemas.PostResponse(**post)
    posts_list = list(map(validate, res.json()))
    assert len(posts_list) == len(test_posts)
    assert res.status_code == 200


def test_users_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    
    post = schemas.PostResponse(**res.json())

    assert post.title == test_posts[0].title
    assert post.content == test_posts[0].content
    assert post.id == test_posts[0].id


@pytest.mark.parametrize(
        'title, content, published',
        [
            ('New Title', 'added new title', True),
            ('Something', 'Here is something interesting', False),
            ('Interesting title', 'Nice one ', False)
        ]
        )
def test_create_posts(client, title, content, published):
    res = client.post(
        '/posts',
        json={'title': title, 'content': content, 'published': published}
    )
    post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published


def test_delete_post(client, test_posts):
    res = client.delete(
        f'/posts/{test_posts[0].id}'
    )

    assert res.status_code == 204


def test_delete_post_non_exist(client):
    res = client.delete('/posts/808080808')

    assert res.status_code == 404


def test_update_post(client, test_posts):
    data = {
            'title': 'Update Title',
            'content': 'Update content'
        }
    res = client.put(
        f'/posts/{test_posts[0].id}',
        json=data
    )

    post = schemas.PostResponse(**res.json())

    assert post.title == data['title']
    assert post.content == data['content']
    assert post.id == test_posts[0].id


def test_update_post_non_exist(client):
    data = {
            'title': 'Update Title',
            'content': 'Update content'
        }
    res = client.put(
        '/posts/980090',
        json=data
    )

    assert res.status_code == 404
