from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

#models.Base.metadata.create_all(bind=engine)
origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.app)
app.include_router(user.app)
app.include_router(auth.router)
app.include_router(vote.app)

@app.get("/")
async def root():
    return {"Greeting":"Welcome, This is social media API"}