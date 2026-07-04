from .. import schemas
from fastapi import  Response, HTTPException, status, Depends, APIRouter
from ..database import get_db
from .. import models
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..oauth2 import get_current_user

app = APIRouter(prefix="/posts",tags=["Post"])


@app.get("",response_model=List[schemas.PostOut])
async def get_(db: Session = Depends(get_db),id: int=Depends(get_current_user), limit: int= 2, search: Optional[str] = ""):
    #posts = db.query(models.Post)
    posts = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.content.contains(search)).limit(limit)
    formatted_posts = [{"Post": post, "votes": votes} for post, votes in posts]
    return formatted_posts

@app.post("")
async def create_post(p: schemas.post, db: Session = Depends(get_db), user: schemas.UserOut = Depends(get_current_user)):
    p = p.model_dump()
    p["owner_id"] = user.id
    new_post = models.Post(**p)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    if not new_post:
        return {"Invalid post"}
    return {"Message":"Post added successfully"}

@app.get("/{id}",status_code= status.HTTP_201_CREATED, response_model=schemas.PostOut)
def find_post(id , db: Session = Depends(get_db), user: schemas.UserOut = Depends(get_current_user)):
    p = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Post not found")
    return p

@app.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: schemas.UserOut = Depends(get_current_user)):
    p = db.query(models.Post).filter(models.Post.id == id)
    post = p.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized operation")
    p.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.post_reponse)
def update_post(id: int, updated_post: schemas.post, db: Session = Depends(get_db), user : schemas.UserOut =Depends(get_current_user) ):
    p = db.query(models.Post).filter(models.Post.id == id)
    Post = p.first()
    if Post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Message":"Post not found"})
    if Post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized operation")
    p.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return p.first()