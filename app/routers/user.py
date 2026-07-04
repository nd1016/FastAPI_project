from .. import schemas
from fastapi import  HTTPException, status, Depends, APIRouter
from ..database import  get_db
from .. import models
from sqlalchemy.orm import Session
from ..utils import hash

app = APIRouter(prefix="/users",tags=["User"])

@app.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session =Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    if not new_user:
        return {"Invalid User details"}
    return new_user

@app.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def search_user(id: int, db: Session  = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
