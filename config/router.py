from fastapi import APIRouter
from routes.blogguide_users import router as users_router
from routes.post import router as posts_router

blogguide_router = APIRouter()

blogguide_router.include_router(users_router, prefix="/users", tags=["Blogguide - Users"])
blogguide_router.include_router(posts_router, prefix="/posts", tags=["Blogguide - Posts"])
