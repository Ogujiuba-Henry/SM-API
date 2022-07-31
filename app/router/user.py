from fastapi import status, HTTPException,APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router=APIRouter(tags=["Users"])                  # tags separates diff routes in  api documentation


@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):

    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(email=user.email, password=user.password)
    db.add(new_user)   #add it to the databse
    db.commit()         # to push out the changes
    db.refresh(new_user)
    
    # cursor.execute("""INSERT INTO users(email,password) VALUES(%s,%s) RETURNING * """,(user.email,user.password))
    # new_user=cursor.fetchone()
    # conn.commit()

    return new_user

@router.get("/users/{id}",response_model=schemas.UserResponse)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    # cursor.execute("""SELECT * FROM users WHERE id = %s""",(str(id),))
    # user=cursor.fetchone() 

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with {id} not found")
    
    return user
      

