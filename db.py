from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import Table, create_engine, MetaData, Column, Text
from sqlalchemy.schema import DropTable

from typing_extensions import Annotated

# fasapi_sqlalchemy is no longer supported/deprectaed, sowe can
#directly use DBSession
# from fastapi_sqlalchemy import db

from sqlalchemy.sql import select, update, delete, case
from sqlalchemy.orm import scoped_session, sessionmaker

from jose import JWTError, jwt

#import the class correspoding to the Products table
from models import Products, Users

from passlib.context import CryptContext


import config

DBSession = scoped_session(sessionmaker())
engine = None

#creating a context in which context we are going to decrypt the password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#defining a scheme for oauth2 so it can be applied to an auth-verification function
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

def init_session(postgres_url):
    global engine, DBSession
    engine = create_engine(postgres_url, echo=False)
    DBSession.remove()
    DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)

# logger.debug(config.POSTGRES_URL)
init_session(postgres_url=config.POSTGRES_URL)

def list_products():
    products = DBSession.query(Products).all()
    return products

def insert_new_product(new_products_list):
    DBSession.add_all(new_products_list)
    DBSession.commit()
    return True

def delete_product(prod_id):
    #the first() will returnjthe first object from the returned object-list
    my_object = DBSession.query(Products).filter_by(product_id=prod_id).first()
    #my_objects = DBSession.query(Products).filter_by(product_id=prod_id)
    if(my_object and my_object.product_id):
        DBSession.delete(my_object)
        DBSession.commit()
        return True
    return False


def get_password_hash(password):
    return pwd_context.hash(password)

def insert_new_user(new_user):
    new_user[0].user_password = get_password_hash(new_user[0].user_password)
    DBSession.add_all(new_user)
    DBSession.commit()
    return True


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt    


def login_user(user_cred):
    current_user = DBSession.query(Users).filter_by(user_email=user_cred.user_email).first()
    if(current_user and current_user.user_password):
        valid_password = verify_password(user_cred.user_password, current_user.user_password)
        if(valid_password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user_cred.user_email}, expires_delta=access_token_expires
            )
            return access_token
        else: return False
    return False


# if we can ghet the user for that token it mena sthat this token is valid
#async def get_current_user(token: str): (later)
## requires Python 3.9.6 | def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usr_email: str = payload.get("sub")
        if usr_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = DBSession.query(Users).filter_by(user_email=usr_email).first()
    if user is None:
        raise credentials_exception
    return user


# The usee of Annoated can speed execution, but requries Python 3.9.6 minimum
#
# def get_current_active_user(current_user: Users = get_current_user):
#def get_current_active_user(current_user: Annotated[Users, Depends(get_current_user)]):
#    if current_user.disabled:
#        raise HTTPException(status_code=400, detail="Inactive user")
#    return current_user

# def get_current_active_user(current_user: Users = get_current_user):
def get_current_active_user(access_token: str=Header(None)):
    current_user = get_current_user(access_token)
    if not current_user.user_password:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
