from app import schemas
import pytest

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts")
    # def validate(post):
    #     return schemas.PostResponse(**post)
    # posts_map = map(validate,res.json())     || data is stored in res.json()
    assert res.status_code == 200

def test_unauthorized_get_all_posts(client,test_posts):
    res=client.get("/posts")
    assert res.status_code == 401

def test_unauthorized_get_one_post(client,test_posts):
    res=client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
    res=authorized_client.get(f"/posts/555")
    assert res.status_code == 404


def test_get_one_post(authorized_client,test_posts):
    res=authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())        # to check if it obeyed all our schema validations
    assert post.Post.id ==test_posts[0].id     # post.Post because Post schema contains all our required schema fields
    assert post.Post.content ==test_posts[0].content
    assert post.Post.title ==test_posts[0].title


@pytest.mark.parametrize("title,content,published",[
    ("my first new post","my first new content", True),
    ("my second new post","my second new content", False),
    ("my third new post","my third new content", True)
])
def test_create_new_post(authorized_client,test_user,title,content,published):
    res = authorized_client.post("/posts", json={"title":title,"content":content,"published":published})
    created_post=schemas.PostResponse(**res.json())   #validate the pydanctic response and unpack the res and convert to json

    assert res.status_code ==201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]

def test_create_post_default_published_true(authorized_client,test_user):
    res = authorized_client.post("/posts", json={"title":"test title","content":"test content"})
    created_post=schemas.PostResponse(**res.json())   #validate the pydanctic response and unpack the res and convert to json

    assert res.status_code ==201
    assert created_post.title == "test title"
    assert created_post.content == "test content"
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]

def test_unauthorized_create_posts(client,test_posts):
    res = client.post("/posts", json={"title":"test title","content":"test content"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/777776")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")        #test_post[3] belongs to test_user2 and we are automatically logged in as test_user
    assert res.status_code == 403


def test_update_post(authorized_client,test_user,test_posts):
    data_update = {
        "title":"Updated new title",
        "content": "Updated new content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}",json=data_update)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data_update["title"]
    assert updated_post.content == data_update["content"]

def test_update_other_user_post(authorized_client,test_user,test_posts):
    data_update = {
        "title":"Updated new title",
        "content": "Updated new content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}",json=data_update)

    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_posts):
    res = client.put(f"/posts/{test_posts[0].id}",json={"title":"wont matter","content":"wont matter too"})
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client,test_user,test_posts):
    data_update = {
        "title":"Updated new title",
        "content": "Updated new content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/8000",json = data_update)
    assert res.status_code == 404