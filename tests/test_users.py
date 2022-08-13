from app import schemas
import pytest
from jose import jwt
from app.config import settings


def test_root(client,session):
    res=client.get("/")                                                                     #testing get method /
    assert res.json().get('message') == "Welcome to my api"
    assert res.status_code==200

def test_user_create(client,session):
    res = client.post("/users",json={"email":"hello12@gmail.com","password":"password123"})
    print(res.json())
    new_user=schemas.UserResponse(**res.json())       #** || unpacking our data in dict() form and create new pydanctic class stored in new_user
    assert new_user.email == "hello12@gmail.com"
    assert res.status_code == 201

def test_user_login(client,test_user):                                                                     #dependent on client fixture
    res = client.post("/login", data={"username":test_user["email"],"password":test_user["password"]})  # data not json bcos we use form-data format
    login_res = schemas.Token(**res.json())
    payload=jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])

    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code",[      # for testing correct emailagainst wrong password and vice versa
    ("wrongemail@gmail.com","password123",403),
    ("hello12@gmail.com","wrongpassword",403),
    ("hello12@gmail.com",None,422)      #422 is correct bcos it fails missing field validation
])

def test_incorrect_login(test_user,client,email,password,status_code):
    res = client.post("/login" ,data={"username":email,"password":password})
    assert res.status_code == status_code
    # assert res.json().get("detail") =="Invalid Credentials"


