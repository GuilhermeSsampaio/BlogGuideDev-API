# Re-exporta tudo dos módulos separados para manter compatibilidade
# com imports existentes: from repository.crud import X

from repository.user_crud import *       # noqa: F401,F403
from repository.post_crud import *       # noqa: F401,F403
from repository.forum_crud import *      # noqa: F401,F403
from repository.comentario_crud import * # noqa: F401,F403
from repository.curtida_crud import *    # noqa: F401,F403
from repository.admin_crud import *      # noqa: F401,F403
from repository.vaga_crud import *       # noqa: F401,F403
from repository.search_crud import *     # noqa: F401,F403
from repository.conteudo_crud import *   # noqa: F401,F403
from repository.notificacao_crud import * # noqa: F401,F403
from repository.sugestao_crud import * # noqa: F401,F403

