from databas import engine , SessionLocal
from fastapi import FastAPI , HTTPException , Depends , status
import amniat
from amniat import decod_token
import models
from models import City , Users
from sqlalchemy.orm import Session
from pydantic import BaseModel 
from typing import Annotated

app = FastAPI()

varify_user = Annotated[dict , Depends(decod_token)]

models.Base.metadata.create_all(bind=engine)
name_of_cities = ['ahvaz' , 'tehran', 'esfehan' , 'yazd' , 'ghom' , 'tabriz'] 

app.include_router(amniat.router)

def op_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
      

class get_hava(BaseModel):
    date : str
    status : str
    name : str




@app.get("/admin/get_all" , tags= [ "admin"] , status_code= status.HTTP_200_OK, description="this part is only for admins")
async def get_users(user : varify_user,db : Annotated[Session , Depends (op_db)]):
        if user is None or db.query(Users).filter(user.get("id") == Users.id).first().admin == False:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        return db.query(Users).all()


@app.post('/add_hava' , tags= ["havashenas"] , status_code= status.HTTP_200_OK , description= "this part is only for havashenas")  
async def hava(city_hava : get_hava ,user : varify_user , db : Annotated[ Session , Depends(op_db)]):
    if user is None or db.query(Users).filter(user.get("id") == Users.id).first().havashenas == False:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    if city_hava.name is None :
        raise HTTPException (status_code= 401 , detail="you have to write name of city")
    for i in name_of_cities :
        if city_hava.name != i :
            raise HTTPException (status_code= 401 , detail="you have to write right name of city")
    add_model = City(
        date = city_hava.date, 
        name = city_hava.name,
        status = city_hava.status
    )

    db.add(add_model)
    db.commit()


@app.get('/get_user_by_id' , tags= ["admin"] , status_code= status.HTTP_200_OK , description= "this part is only for admins")
async def hava(user_id : int , user : varify_user , db : Annotated[ Session , Depends(op_db)]):
    if user is None or db.query(Users).filter(user.get("id") == Users.id).first().admin == False:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user_id).first()


@app.delete("/admin/delete_user" , tags= ["admin"] , status_code= status.HTTP_200_OK,
            description="this function is just for admins so if you are not admin your Authentication will be Failed ")
async def hava( user_id : int,user : varify_user , db : Annotated[ Session , Depends(op_db)]):
    if user is None or db.query(Users).filter(user.get("id") == Users.id).first().admin == False:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db.query(Users).filter(user_id == Users.id).delete()
    db.commit()

@app.delete("/havashenas/delete_gozaresh" , tags= ["havashenas"] , status_code= status.HTTP_200_OK,
            description="this function is just for havashenas so if you are not admin your Authentication will be Failed ")
async def hava( gozaresh_id : int ,user : varify_user , db : Annotated[ Session , Depends(op_db)]):
    if user is None or db.query(Users).filter(user.get("id") == Users.id).first().havashenas == False:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db.query(City).filter(gozaresh_id == City.id).delete()
    db.commit()

@app.get('/get_gozaresh_by_id' , tags= ["havashenas"] , status_code= status.HTTP_200_OK , description= "this part is only for havashenas")
async def hava(gozaresh_id : int , user : varify_user , db : Annotated[ Session , Depends(op_db)]):
    if user is None or db.query(Users).filter(user.get("id") == Users.id).first().havashenas == False:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(City).filter(City.id == gozaresh_id).first()
