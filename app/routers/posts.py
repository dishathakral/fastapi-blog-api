from fastapi import status,HTTPException,Depends,APIRouter
from .. import database_models,models,oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router=APIRouter()


@router.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post1:models.PostCreate,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    print(current_user)
    new_entry=database_models.Post(**post1.dict(), owner_id=current_user.id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry) #gives output to user like returning statement of sql
    # cursor.execute('''insert into posts(name,content,published) values (%s,%s,%s) returning *''',(post1.title,post1.content,post1.published))
    # new_post_created=cursor.fetchone()
    # conn.commit()
    return new_entry

@router.get("/posts",response_model=List[models.PostResponse])
@router.get("/posts")
def get_posts(db: Session = Depends (get_db),limit : int=10,skip:int=0, search : Optional[str]=""):
    # cursor.execute('''select * from posts''')
    # post=cursor.fetchall()
    # post=db.query(database_models.Post).filter(database_models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results=db.query(database_models.Post,func.count(database_models.Vote.user_id).label("vote_count")).join(database_models.Vote,database_models.Vote.post_id==database_models.Post.id,isouter=True).group_by(database_models.Post.id).all()
    print(results)
    return results

@router.get("/posts/{id}",response_model=models.PostResponse)
def get_post(id:int,db: Session = Depends (get_db)):


    results = db.query(database_models.Post, func.count(database_models.Vote.user_id).label("vote_count")).join(
        database_models.Vote, database_models.Vote.post_id == database_models.Post.id, isouter=True).group_by(
        database_models.Post.id).filter(database_models.Post.id==id).first()

    recent_post=db.query(database_models.Post).filter(database_models.Post.id==id).first()
    # cursor.execute('''select * from posts where post_id=%s''',(id,))
    # recent_post=cursor.fetchone()
    if not recent_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    print(results)
    post, vote_count = results
    print(post)
    print(vote_count)
    return {"Post":post, "votes": vote_count}

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends (get_db),user_id:int = Depends(oauth2.get_current_user)):
    deleted_post=db.query(database_models.Post).filter(database_models.Post.id==id)
    post=deleted_post.first()
    # cursor.execute('''delete from posts where post_id=%s returning *''',(id,))
    # delted_post=cursor.fetchone()
    # conn.commit()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    if user_id.id!=post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return(f"post_id:{id} successfully deleted!!!")


#path operation to update post using put http method
@router.put("/posts/{id}")
def update_post(id:int,post:models.PostCreate,db: Session = Depends (get_db),user_id:int = Depends(oauth2.get_current_user)):
    post_query=db.query(database_models.Post).filter(database_models.Post.id==id)
    updated_post=post_query.first()
    print("user_id:", user_id)  # check if it's dict, object, or int
    print("updated_post.owner_id:", updated_post.owner_id)
    # cursor.execute('''update posts set name=%s,content=%s,published=%s where post_id=%s returning *''',(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    if user_id.id!=updated_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return(f"post id:{id} this is updated!")