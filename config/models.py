def setup_models():
    """
    Importa todos os modelos da aplicação para que o SQLModel
    possa registrá-los no metadata antes da criação das tabelas.
    """

    # Módulo de Autenticação
    from auth.models.user import User  # noqa: F401
    from auth.models.auth_provider import AuthProvider  # noqa: F401

    # Módulo CookAI
    from models.blogguide_user import BlogguideUser  # noqa: F401
    from models.post import Post  # noqa: F401
    from models.forum import Forum  # noqa: F401
    from models.comentario import Comentario  # noqa: F401
    from models.curtida import Curtida  # noqa: F401
    from models.vaga import Vaga  # noqa: F401