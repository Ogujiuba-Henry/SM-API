from app.database import get_db, Base
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
import pytest
from app.oauth import create_access_token
from app import models
# from alembic import command

SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL) #establishing the connection to postgres database

Test_SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine) # talking to the database || allows to make queries to db


client = TestClient(app)     #referencing our fastapi instance app

@pytest.fixture()
def session():
     Base.metadata.drop_all(bind=engine)                                            #drop any existing table
     Base.metadata.create_all(bind=engine)                                          #create table to run tests
     db=Test_SessionLocal()
     try:
         yield db
     finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():       # create a session anytime we get a request to our database with override_db
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db   #swap get_db with overide_get_db
    yield TestClient(app)



# a fixture function that creates a another new user to test login
@pytest.fixture
def test_user2(client):              
    user_data = {"email":"what_up@gmail.com","password":"password123"} 
    res=client.post("/users",json=user_data)

    # assert res.status_code ==201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]      #to add password as part of data returned in res.json()
    return new_user

# a fixture function that creates a brand new user to test login
@pytest.fixture
def test_user(client):              
    user_data = {"email":"hello12@gmail.com","password":"password123"} 
    res=client.post("/users",json=user_data)

    # assert res.status_code ==201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]      #to add password as part of data returned in res.json()
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})       #function returns a token for verifying a user 

@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,"Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture                   # to create a fixture containing posts we can use to test get all/one post
def test_posts(test_user,session,test_user2):
    # posts_data = [
    #     {"title":"first title",
    #     "content":"first content",
    #     "user_id":test_user["id"]
    #     },

    #     {"title":"second title",
    #     "content":"second content",
    #     "user_id":test_user["id"]
    #     },

    #     {"title":"third title",
    #     "content":"third content",
    #     "user_id":test_user["id"]
    #     }

    # ]
    
    # to add some sample post to use and test
    session.add_all([models.Post(title="first title",content="first content",user_id=test_user["id"]),
    models.Post(title="second title title",content="second content",user_id=test_user["id"]),
    models.Post(title="third title",content="third content",user_id=test_user["id"]),
    models.Post(title="fourth title title",content="fourth content",user_id=test_user2["id"])])  # last post was created to belong to test_user2 to test del other user func 

    session.commit()  # to send the posts to pg database

    posts = session.query(models.Post).all()     #to get all the data back like sqlalchemy

    return posts



    # def create_post_model(post):
    #     return models.Post(**post)

    # post_map = map(create_post_model,posts_data)

    # posts=list(post_map)

    # session.add_all(posts)
    # session.commit()

    # posts = session.query(models.Post).all()
    
    # return posts


