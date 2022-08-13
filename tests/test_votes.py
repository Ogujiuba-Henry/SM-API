import pytest
from app import models

@pytest.fixture                  # func votes on a post[id=3]
def test_vote(test_posts,session,test_user):    # import session bcos we'll be making vote changes directly to db
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()

def test_vote_post(authorized_client,test_posts):
    res = authorized_client.post("/vote",json={"post_id":test_posts[0].id, "dir":1})
    assert res.status_code == 201

def test_vote_on_post_twice(authorized_client,test_posts,test_vote):
    res = authorized_client.post("/vote",json={"post_id":test_posts[3].id, "dir": 1})
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote",json={"post_id":test_posts[3].id, "dir": 0})
    assert res.status_code == 201

def test_delete_vote_non_exist(authorized_client,test_posts):
    res = authorized_client.post("/vote",json={"post_id":test_posts[3].id, "dir": 0})
    assert res.status_code == 404

def test_vote_non_exist(authorized_client,test_posts):
    res = authorized_client.post("/vote",json={"post_id":8000, "dir": 1})
    assert res.status_code == 404

def test_vote_unauthenticated_user(client,test_posts):
    res = client.post("/vote",json={"post_id":test_posts[3].id, "dir": 1})
    assert res.status_code == 401
