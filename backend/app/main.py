from fastapi import FastAPI
from app.api.routes.events import router as event_router
from app.exceptions.handlers import register_exception_handlers
from app.middleware.logging_middleware import LoggingMiddleware
from app.api.routes.dashboard import router as dashboard_router
app = FastAPI(
    title="Intelligent Video Serveillance System",
    version="1.0.0"
)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

app.include_router(dashboard_router)

app.include_router(event_router)

@app.get("/")
def root():
    return {
        "message":"Welcome to Intelligent Video Serveillance System 🚀"
    }