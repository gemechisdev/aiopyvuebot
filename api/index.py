import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

from .routes import telegram

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="WhispierBot API",
        version="1.0.0",
        description="API for WhispierBot - Send secret whisper messages",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Initialize FastAPI
app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url=None,
    redoc_url=None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = custom_openapi

# Include routers
app.include_router(telegram.router)


@app.get("/api/docs", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="WhispierBot API Documentation",
        swagger_favicon_url="/favicon.ico"
    )


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    from .db import supabase

    bot_status = "configured" if telegram.TOKEN else "not configured"
    db_status = "connected" if supabase else "not connected"

    return {
        "status": "healthy",
        "bot": "whispierbot",
        "bot_status": bot_status,
        "database_status": db_status,
        "message": "WhispierBot API is running!"
    }