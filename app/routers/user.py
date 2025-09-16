from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from .. import database_models,models,utils
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter()

#path to create user
@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=models.Userout)
def create_user(user:models.Usercreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_entry=database_models.User(**user.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry 
#path to access user details
@router .get("/users/{id}",response_model=models.Userout)
def get_post(id:int,db: Session = Depends (get_db)):
    user=db.query(database_models.User).filter(database_models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return user