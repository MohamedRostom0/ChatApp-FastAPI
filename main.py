from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.api.auth import router as auth_router
from app.db.mongodb import get_db

app = FastAPI()

app.include_router(api_router)
app.include_router(auth_router)


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