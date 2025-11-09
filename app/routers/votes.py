from fastapi import status,HTTPException,Depends,APIRouter
from .. import database_models,models,oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter()
@router.post("/vote",status_code=status.HTTP_201_CREATED)
def post_vote(vote:models.vote,db: Session = Depends (get_db),current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(database_models.Post).filter(database_models.Post.id == vote.post_id). first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote. post_id} does not exist")
    vote_query=db.query(database_models.Vote).filter(database_models.Vote.user_id==current_user.id,database_models.Vote.post_id==vote.post_id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")
        new_vote=database_models.Vote(user_id=current_user.id,post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote doesn't exist!")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted the vote"}