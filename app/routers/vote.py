from fastapi import HTTPException, status, Depends, APIRouter
from .. import schemas, database
from .. import models
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user


app = APIRouter(prefix="/vote",tags=["Vote"])

@app.post("")
def vote_func(vote: schemas.vote, db: Session = Depends(database.get_db), user: schemas.UserOut = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    votes_q = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == user.id )
    if vote.dir == 1:
        if votes_q.first() :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted for this post")
        votes = models.Votes(post_id = vote.post_id, user_id = user.id)
        db.add(votes)
        db.commit()
        return {"Message":"Successfully voted"}

    else:
        if not votes_q.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        votes_q.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}