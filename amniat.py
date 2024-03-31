from datetime import timedelta, datetime
from typing import Annotated 
from fastapi import APIRouter, Depends, HTTPException 
from pydantic import BaseModel , Field
from sqlalchemy.orm import Session
from starlette import status
from databas import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt , JWTError
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'

admin_password = "80344fe73b8flr57a65"
havashenas_password = "49253fe73b8gm4lsp60"

create_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
bearer = OAuth2PasswordBearer(tokenUrl='auth/enter')

def op_db ():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()


# def varfy_user(  user_name ,password: str , db ):
#     user = db.query(Users).filter(Users.username == user_name).first()
#     if not user:
#         return False
#     if not create_context.verify(password, user.hashed_password):
#         return False
#     return user


class create_user(BaseModel):
    __tablename__ = 'users'

    email : str = Field( min_length= 4,max_length=50 )
    username : str = Field( min_length= 0,max_length=50)
    password : str
    city : str = Field( min_length= 1 ,max_length=50)



def create_token(user_name : str , id : int  ,time_accses : timedelta ):
    encode = {"user_name" : user_name , "id": id   }
    time_exist_of_token  = datetime.utcnow() + time_accses
    json_time = jsonable_encoder(time_exist_of_token)
    encode.update({"time":json_time })
    return jwt.encode(encode , SECRET_KEY , algorithm= ALGORITHM)



async def decod_token(token: Annotated[str, Depends(bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get('user_name')
        id: int = payload.get('id')

        if user_name is None or id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail='Could not validate user.')
        return {'username': user_name, 'id': id}
    except JWTError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Could not validate user.')
    

@router.post("/enter" , status_code=status.HTTP_200_OK  )
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db:  Annotated[Session , Depends (op_db)]):
    
    user_name = db.query(Users).filter(Users.username == form_data.username).first()
    if not user_name:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    user_pass = db.query(Users).filter(Users.username == form_data.username).first()
    
    if not user_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

    token_auth = create_token(user_name.username , user_name.id ,timedelta(minutes= 30))
    return {'access_token': token_auth, 'token_type': 'bearer'}


@router.post("/users/create_accont" ,status_code= status.HTTP_200_OK)
async def create_user(db : Annotated[Session , Depends (op_db)] , request : create_user):
    if request.email == Users.email:
        raise HTTPException (status_code= 401 , detail="this accont alredy exist")
    if request.username == Users.username:
        raise HTTPException (status_code= 401 , detail="this username alredy exist please chose enother username")
    if request.password == admin_password  :
        add_model = Users(
        email = request.email,
        username = request.username,
        hashed_password = create_context.hash(request.password),
        city = request.city, 
        admin = True,
        havashenas = False
        )
        db.add(add_model)
        db.commit()

    if request.password == havashenas_password :
        add_model = Users(
        email = request.email,
        username = request.username,
        hashed_password =  create_context.hash(request.password),
        city = request.city, 
        admin = False,
        havashenas = True
        )
        db.add(add_model)
        db.commit()

    else:
        add_model = Users(
        email = request.email,
        username = request.username,
        hashed_password = create_context.hash(request.password),
        city = request.city, 
        admin = False,
        havashenas = False
        )
        db.add(add_model)
        db.commit()