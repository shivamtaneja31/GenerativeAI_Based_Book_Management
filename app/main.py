from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
import logging

from app.config import settings
from app.api.routes import book_routes, review_routes, ai_routes
from app.api.auth import get_current_active_user
from app.utils.logger import setup_logging

# Setup logging
logger = setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable default redoc
)

# CORS configuration
origins = ["*"]  # In production, restrict this to specific domains

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Swagger UI with authentication
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} - API Documentation",
    )

# Application startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Intelligent Book Management System")

# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Intelligent Book Management System")

# Include API routers
app.include_router(
    book_routes.router,
    prefix=f"{settings.API_V1_STR}/books",
    tags=["books"],
)
app.include_router(
    review_routes.router,
    prefix=f"{settings.API_V1_STR}/books",
    tags=["reviews"],
)
app.include_router(
    ai_routes.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["ai"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Intelligent Book Management System API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}