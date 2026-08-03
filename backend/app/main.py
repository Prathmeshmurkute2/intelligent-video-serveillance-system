from fastapi import FastAPI
from app.api.routes.events import router as event_router

app = FastAPI(
    title="Intelligent Video Serveillance System",
    version="1.0.0"
)

app.include_router(event_router)

@app.get("/")
def root():
    return {
        "message":"Welcome to Intelligent Video Serveillance System 🚀"
    }