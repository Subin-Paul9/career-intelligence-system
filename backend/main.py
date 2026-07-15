from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import API routers
from app.routers import auth
from app.routers import users
from app.routers import resume
from app.routers import recommendation_router


app = FastAPI(
    title="Career Intelligence API",
    description="Backend services for user authentication, profile management, and AI-powered career intelligence modules.",
    version="1.0.0",
)


# Serve uploaded resume files
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)


@app.get("/")
def root() -> dict:
    """
    Root endpoint to verify that the backend server is running.
    """
    return {
        "success": True,
        "message": "Career Intelligence Backend is running successfully."
    }


@app.get("/health")
def health_check() -> dict:
    """
    Health check endpoint.
    Used to verify that the backend service is operational.
    """
    return {
        "status": "healthy"
    }


# Authentication APIs
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)


# User Management APIs
app.include_router(
    users.router,
    prefix="/api/users",
    tags=["Users"]
)


# Resume Management APIs
app.include_router(
    resume.router,
    prefix="/api/resume",
    tags=["Resume"]
)


# Career Recommendation APIs
app.include_router(
    recommendation_router.router
)