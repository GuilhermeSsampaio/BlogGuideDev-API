from database import create_db_and_tables, get_session
from models.user import User, UserCreate
from models.post import Post, PostCreate
from sqlmodel import select
from auth.security import get_password_hash
import json

def test_user_operations():
    """Testar operações CRUD de usuários"""
    print("👤 Testando operações de usuários...")
    
    try:
        with next(get_session()) as session:
            # Criar usuário
            user_data = UserCreate(
                name="João Silva",
                username="joao123",
                email="joao@example.com",
                password="senha123",
                bio="Desenvolvedor Python"
            )
            
            # Hash da senha
            hashed_password = get_password_hash(user_data.password)
            
            # Criar usuário no banco
            db_user = User(
                name=user_data.name,
                username=user_data.username,
                email=user_data.email,
                password_hash=hashed_password,
                bio=user_data.bio
            )
            
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            
            print(f"  ✅ Usuário criado: ID {db_user.id}, Nome: {db_user.name}")
            
            # Buscar usuário
            statement = select(User).where(User.email == "joao@example.com")
            found_user = session.exec(statement).first()
            
            if found_user:
                print(f"  ✅ Usuário encontrado: {found_user.username}")
            else:
                print("  ❌ Usuário não encontrado")
                return False
            
            return db_user.id
            
    except Exception as e:
        print(f"  ❌ Erro nas operações de usuário: {e}")
        return False

def test_post_operations(user_id):
    """Testar operações CRUD de posts"""
    print("📝 Testando operações de posts...")
    
    try:
        with next(get_session()) as session:
            # Criar post
            tags = ["python", "fastapi", "tutorial"]
            
            db_post = Post(
                title="Meu Primeiro Post PostgreSQL",
                category="Tutorial",
                content="Este é um post de teste para verificar se o PostgreSQL está funcionando corretamente com todos os campos.",
                author_id=user_id,
                image_url="https://example.com/image.jpg",
                tags=json.dumps(tags),
                is_published=True
            )
            
            session.add(db_post)
            session.commit()
            session.refresh(db_post)
            
            print(f"  ✅ Post criado: ID {db_post.id}, Título: {db_post.title}")
            
            # Buscar post
            statement = select(Post).where(Post.author_id == user_id)
            found_post = session.exec(statement).first()
            
            if found_post:
                # Verificar tags
                post_tags = json.loads(found_post.tags) if found_post.tags else []
                print(f"  ✅ Post encontrado: {found_post.title}")
                print(f"  ✅ Tags: {post_tags}")
                print(f"  ✅ Data criação: {found_post.created_at}")
            else:
                print("  ❌ Post não encontrado")
                return False
            
            return True
            
    except Exception as e:
        print(f"  ❌ Erro nas operações de post: {e}")
        return False

def test_relationships():
    """Testar relacionamentos entre tabelas"""
    print("🔗 Testando relacionamentos...")
    
    try:
        with next(get_session()) as session:
            # Buscar posts com informações do autor
            statement = select(Post, User).join(User)
            results = session.exec(statement).all()
            
            for post, user in results:
                print(f"  ✅ Post '{post.title}' por {user.name} ({user.email})")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Erro nos relacionamentos: {e}")
        return False

def clean_test_data():
    """Limpar dados de teste"""
    print("🧹 Limpando dados de teste...")
    
    try:
        with next(get_session()) as session:
            # Deletar posts de teste
            statement = select(Post).where(Post.title.contains("PostgreSQL"))
            posts = session.exec(statement).all()
            for post in posts:
                session.delete(post)
            
            # Deletar usuários de teste
            statement = select(User).where(User.email == "joao@example.com")
            users = session.exec(statement).all()
            for user in users:
                session.delete(user)
            
            session.commit()
            print("  ✅ Dados de teste removidos")
            
    except Exception as e:
        print(f"  ❌ Erro ao limpar dados: {e}")

if __name__ == "__main__":
    print("🧪 Testando operações CRUD completas...")
    print("=" * 60)
    
    # Criar tabelas
    create_db_and_tables()
    
    # Executar testes
    user_id = test_user_operations()
    
    if user_id:
        if test_post_operations(user_id):
            test_relationships()
    
    # Limpar dados de teste
    clean_test_data()
    
    print("=" * 60)
    print("✅ Testes CRUD concluídos!")