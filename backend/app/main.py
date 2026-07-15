from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.interaction import router as interaction_router
from app.database.database import Base, engine
from app.models.interaction import Interaction
from app.api.ai import router as ai_router
# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI CRM Backend",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register API routes
app.include_router(interaction_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "AI CRM Backend is Running 🚀"
    }