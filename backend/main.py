from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.rate_limiter import limiter

# Import API routers
from app.routers import auth
from app.routers import users
from app.routers import resume
from app.routers import recommendation_router
from app.routers import ai_assistant_router


app = FastAPI(
    title="Career Intelligence API",
    description="Backend services for user authentication, profile management, and AI-powered career intelligence modules.",
    version="1.0.0",
)

# -------------------------
# Rate Limiter Configuration
# -------------------------
app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware,
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    """
    Return a custom response when the rate limit is exceeded.
    """

    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please try again later."
        },
    )


# -------------------------
# Static Files
# -------------------------
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
        "message": "Career Intelligence Backend is running successfully.",
    }


@app.get("/health")
def health_check() -> dict:
    """
    Health check endpoint.
    Used to verify that the backend service is operational.
    """

    return {
        "status": "healthy",
    }


# -------------------------
# Authentication APIs
# -------------------------
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"],
)


# -------------------------
# User Management APIs
# -------------------------
app.include_router(
    users.router,
    prefix="/api/users",
    tags=["Users"],
)


# -------------------------
# Resume Management APIs
# -------------------------
app.include_router(
    resume.router,
    prefix="/api/resume",
    tags=["Resume"],
)


# -------------------------
# Career Recommendation APIs
# -------------------------
app.include_router(
    recommendation_router.router,
)


# -------------------------
# AI Assistant APIs
# -------------------------
app.include_router(
    ai_assistant_router.router,
)