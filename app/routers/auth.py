from .. import schemas
from fastapi import  HTTPException, status, Depends, APIRouter
from ..database import  get_db
from .. import models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordRequestForm

router = APIRouter(tags=["login"],prefix="/login")


@router.post("",status_code=status.HTTP_200_OK, response_model=schemas.token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    token_dict = {"userid":user.id}
    token = oauth2.create_access_token(token_dict)
    
    return {"token": token ,"token_type":  "bearer"}