from fastapi import FastAPI

app = FastAPI(
    title="Intelligent Video Serveillance System",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message":"Welcome to Intelligent Video Serveillance System 🚀"
    }