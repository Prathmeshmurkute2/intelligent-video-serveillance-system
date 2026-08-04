from fastapi import FastAPI
from app.api.routes.events import router as event_router
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(
    title="Intelligent Video Serveillance System",
    version="1.0.0"
)

register_exception_handlers(app)

app.include_router(event_router)

@app.get("/")
def root():
    return {
        "message":"Welcome to Intelligent Video Serveillance System 🚀"
    }