import logging
import time
import uuid
from contextvars import ContextVar

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Match

from apps.candidates.api.v1 import candidate_router
from apps.users.api.v1 import user_router
from elevatus_poc.core.config import settings, Settings
from elevatus_poc.core.logs import setup_logging

logger = logging.getLogger(__name__)


def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/"
    )
    origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    if settings.DEBUG is True:
        origins = ["*"]
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
request_id_contextvar = ContextVar("request_id", default=None)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    status_code = exc.status_code if hasattr(exc, 'status_code') else 500
    logger.error(
        "ElevatusHTTPException raised. Request: %s, user: %s. Error: %s, Code: -1, Status: %s",
        request.url.path, request.scope.get('auth', None), exc.__dict__, status_code
    )
    return JSONResponse(
        {"message": exc.__dict__.get('message', "Something went wrong"), "error_code": -1},
        status_code=status_code,
    )


@app.middleware("http")
async def request_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    request_url = str(request.url)
    request_id_contextvar.set(request_id)
    request_method = request.method
    start_time = time.time()
    logger.info(f"Request started, Method:{request_method}, URL: {request_url}")
    routes = request.app.router.routes
    logger.debug("Request Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    logger.debug("Request Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    try:
        return await call_next(request)
    except Exception as ex:
        logger.error(f"Request failed: {ex}")
        raise
    finally:
        logger.info("Time took to process the request and return response is {} sec".format(
            time.time() - start_time
        ))
        logger.info(f"Request Ended, Method:{request_method}, URL: {request_url}")


@app.on_event("startup")
async def startup_event():
    setup_logging()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(user_router)
app.include_router(candidate_router)
