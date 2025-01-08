from fastapi import FastAPI
from .api.v1.router import router as audio_router
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(audio_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Project!"}
