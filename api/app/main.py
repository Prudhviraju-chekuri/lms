from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import re

from app.core.config import get_config
from app.middleware.error_handler import error_handler
from app.middleware.not_found import not_found_handler
from app.routers import all_routers

# Init app
app = FastAPI()

# Middlewares (CORS)
origins = [get_config("FRONTEND_URL", "*")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logging.info(f"{request.method} {request.url}")
        response = await call_next(request)
        return response

app.add_middleware(LoggingMiddleware)

# 🔥 Middleware to normalize duplicate slashes
class SlashNormalizerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        scope = request.scope
        path = scope.get("path", "")
        # Replace multiple slashes with a single slash
        normalized_path = re.sub(r"/+", "/", path)
        if normalized_path != path:
            scope["path"] = normalized_path
        return await call_next(request)

app.add_middleware(SlashNormalizerMiddleware)

# Routers
for prefix, router in all_routers:
    app.include_router(router, prefix=prefix)

# Error handlers
app.add_exception_handler(Exception, error_handler)
app.add_exception_handler(404, not_found_handler)

@app.get("/")
def root():
    return {"message": "Python backend running!"}
