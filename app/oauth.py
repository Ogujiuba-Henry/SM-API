from fastapi import Depends, status,HTTPException,status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode=data.copy()                        # to make a copy of the data from create_token func above

    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})     #to make sure were adding the expire property into our to_encode variable

    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)   #this will encode all the to_encode data

    return encoded_jwt


def verify_access_token(token:str,credentials_exception):

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id:str=payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data=schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data

def  get_current_user(token:str = Depends(oauth_scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token,credentials_exception)

    user=db.query(models.User).filter(models.User.id==token.id).first()

    return user