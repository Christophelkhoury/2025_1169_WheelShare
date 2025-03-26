from fastapi import FastAPI, Depends
from app.api import trips, properties, chat, upload
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.core.database import get_db
import os

load_dotenv()

app = FastAPI()

# CORS
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(trips.router, prefix="/trips")
app.include_router(properties.router, prefix="/properties")
app.include_router(chat.router, prefix="/chat")
app.include_router(upload.router, prefix="/upload")

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/test-db")
def test_db(db = Depends(get_db)):
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"message": f"Database connection failed: {str(e)}"}
