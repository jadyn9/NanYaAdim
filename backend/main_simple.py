from fastapi import FastAPI

app = FastAPI(
    title="Test API",
    version="1.0.0",
    description="Test API for backend service"
)


@app.get("/")
def root():
    """
    Root endpoint
    """
    return {"message": "Welcome to Test API", "status": "running"}


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}
