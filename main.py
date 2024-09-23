from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.db.mongodb import get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_router)
app.include_router(chat_router)


# Dependency Injection for database
@app.on_event("startup")
async def startup_db_client():
    app.mongodb = get_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb.client.close()

# Root path for the API
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Chat API!"}