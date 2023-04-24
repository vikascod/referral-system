from fastapi import FastAPI
from app import models
from app.database import Base, engine
from app.routers import user, auth, referral
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(engine)

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return "Welcome To Home"


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(referral.router)