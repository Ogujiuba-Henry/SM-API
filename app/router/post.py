from app.database import get_db
from typing import List, Optional
from fastapi import status, HTTPException,APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from .. import models,schemas,oauth
from ..database import get_db
from sqlalchemy import func


router=APIRouter(tags=["Posts"])

@router.get("/posts",response_model=List[schemas.PostOut]) # retrieve data from /post url || List bcos we were returning a list of posts already and we want a list of our specific response schema post
def get_posts(db: Session = Depends(get_db),user_id:int = Depends(oauth.get_current_user),limit:int = 10,offset:int=0,search:Optional[str]=""):
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()   # same with the PgAdmin sql method
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()  # to execute the sql code
    return posts

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse) 
def create_posts(post:schemas.Post, db: Session = Depends(get_db),current_user:int = Depends(oauth.get_current_user)): #func accepts variable post referencing the Post class

    new_post=models.Post(user_id=current_user.id,title=post.title, content=post.content, published=post.published)
    db.add(new_post)   #add it to the databse
    db.commit()         # to push out the changes
    db.refresh(new_post)     #equivalent to RETURNING * which retrieves the new_post you created and store it back into the variable
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()  # to push the changes out to postgres
    return new_post


@router.get("/posts/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user:int = Depends(oauth.get_current_user)): # to validate that the path parameter is of type int
    # post=db.query(models.Post).filter(models.Post.id==id).first()
    post= posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),)) # str bcos the %s should be a string || , just fixes one kind issue he says
    # post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not found")
    return post


@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    delete_post=db.query(models.Post).filter(models.Post.id==(id))
    deleted_post=delete_post.first()
    # cursor.execute("""DELETE FROM posts where id = %s RETURNING * """,(str(id,)))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exist")

    if deleted_post.user_id != current_user.id:       #to delete  a post belonging to verified logged in user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    delete_post.delete(synchronize_session=False)  # default setting it dont really matter
    db.commit()

    #return @router.put("/posts/{id}",response_model=schemas.PostResponse)
@router.put("/posts/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.Post,db:Session = Depends(get_db),current_user:int = Depends(oauth.get_current_user)):
    updated_post=db.query(models.Post).filter(models.Post.id==(id))
    post_query=updated_post.first()
    # cursor.execute("""UPDATE posts SET  title = %s, content=%s, published=%s WHERE id =%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    if post_query==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exist")
    if post_query.user_id != current_user.id:  # to update a post belonging to verified logged in user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    updated_post.update(post.dict(),synchronize_session=False)
    db.commit()
    return updated_post.first()
    
    #Response(status_code=status.HTTP_204_NO_CONTENT) # So that no error emerges even after index is deleted