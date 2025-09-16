from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from .. import database_models,models,utils,oauth2
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(tags=['authentication'])

@router.post('/login',response_model=models.Token)
def login(user_creedentials:models.Userlogin, db:Session=Depends(get_db)):
    user=db.query(database_models.User).filter(user_creedentials.email==database_models.User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    utils.verify_password(user_creedentials.password,user.password)
    #generate token
    access_token=oauth2.create_access_token(data={'user_id':user.id})
    return {"access_token": access_token, "token_type": "bearer"}
