from fastapi import FastAPI
from app.api.routes.events import router as event_router
from app.exceptions.handlers import register_exception_handlers
from app.middleware.logging_middleware import LoggingMiddleware
from app.api.routes.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.camera import router as camera_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)
app.include_router(camera_router)
app.include_router(dashboard_router)

app.include_router(event_router)

@app.get("/")
def root():
    return {
        "message":"Welcome to Intelligent Video Serveillance System 🚀"
    }