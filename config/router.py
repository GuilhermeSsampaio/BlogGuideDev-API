from fastapi import APIRouter
from routes.blogguide_users import router as users_router
from routes.post import router as posts_router
from routes.conteudos import router as conteudos_router
from routes.forum import router as forum_router
from routes.comentarios import router as comentarios_router
from routes.curtidas import router as curtidas_router
from routes.admin import router as admin_router
from routes.vagas import router as vagas_router
from routes.search import router as search_router

blogguide_router = APIRouter()

blogguide_router.include_router(users_router, prefix="/users", tags=["Blogguide - Users"])
blogguide_router.include_router(posts_router, prefix="/posts", tags=["Blogguide - Posts"])
blogguide_router.include_router(conteudos_router, prefix="/conteudos", tags=["Conteúdos - Público"])
blogguide_router.include_router(forum_router, prefix="/forum", tags=["Fórum"])
blogguide_router.include_router(comentarios_router, prefix="/comentarios", tags=["Comentários"])
blogguide_router.include_router(curtidas_router, prefix="/curtidas", tags=["Curtidas"])
blogguide_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
blogguide_router.include_router(vagas_router, prefix="/vagas", tags=["Vagas"])
blogguide_router.include_router(search_router, prefix="/search", tags=["Pesquisa"])
