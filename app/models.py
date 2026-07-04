from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts" 

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("User.id",ondelete="Cascade"),nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    posts = relationship("Post",back_populates="owner")

class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("User.id", ondelete="Cascade"),nullable=False,primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="Cascade"),nullable=False,primary_key=True)