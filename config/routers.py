from fastapi import FastAPI
from auth.routes.auth_routes import router as auth_router
from auth.routes.oauth_routes import router as oauth_router


from .router import blogguide_router


def setup_routers(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(oauth_router)
    app.include_router(blogguide_router)
