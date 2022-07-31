from fastapi import APIRouter, Depends, FastAPI, status,HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth


router=APIRouter(tags=["Vote"])

@router.post("/vote",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session = Depends(database.get_db), current_user:int = Depends(oauth.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()   
    if not post:                        #to make sure the post actually exists in database
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:(vote.post_id) does not exist")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id ==current_user.id)
    found_vote = vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user{current_user.id} has already liked this post{vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)  #this will set the two parameters;post_id:user_id as in the votetable
        db.add(new_vote)
        db.commit()
        return{"message":"Successfully liked post"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully deleted vote"}

