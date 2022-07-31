from passlib.context import CryptContext

pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto") # hashing algorithm we use

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password,hashed_password):  # comparing user password with db hashed password
    return pwd_context.verify(plain_password,hashed_password)