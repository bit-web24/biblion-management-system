from fastapi import FastAPI
from app.routers import biblion

app = FastAPI(title="Book Management System", version="1.0.0")
app.include_router(biblion.router)

@app.get("/")
async def root():
    return {
        "message": """Task: Build a RESTful API for a simple book management system.
        Requirements:
            1. Use FastAPI to create CRUD endpoints.
            2. Store data in an SQLite or PostgreSQL database using SQLAlchemy.
            3. Implement authentication with OAuth2 or JWT.
        """
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)