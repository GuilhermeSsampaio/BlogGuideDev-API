from database import create_db_and_tables, get_session, engine
from sqlmodel import text
import os
from dotenv import load_dotenv

# Forçar carregamento do .env
load_dotenv(override=True)

def test_connection():
    """Testar conexão com o banco"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"✅ Conexão OK: {result.fetchone()}")
            return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_tables():
    """Testar criação de tabelas"""
    try:
        create_db_and_tables()
        print("✅ Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

def test_basic_operations():
    """Testar operações básicas"""
    try:
        with next(get_session()) as session:
            # Teste adaptativo baseado no tipo de banco
            db_url = os.getenv("DATABASE_URL", "sqlite:///./bloguide.db")
            
            if db_url.startswith("postgresql"):
                # Query específica para PostgreSQL
                result = session.execute(text("SELECT current_database()"))
                db_name = result.fetchone()[0]
                print(f"✅ Banco PostgreSQL: {db_name}")
            else:
                # Query genérica para SQLite
                result = session.execute(text("SELECT 'bloguide' as db_name"))
                db_name = result.fetchone()[0]
                print(f"✅ Banco SQLite: {db_name}")
            
            return True
    except Exception as e:
        print(f"❌ Erro nas operações: {e}")
        return False

def detect_database_type():
    """Detectar tipo de banco configurado"""
    db_url = os.getenv("DATABASE_URL", "sqlite:///./bloguide.db")
    
    if db_url.startswith("postgresql"):
        return "PostgreSQL"
    elif db_url.startswith("mysql"):
        return "MySQL"
    else:
        return "SQLite"

if __name__ == "__main__":
    # Debug das variáveis de ambiente
    print("🔧 Debug das variáveis:")
    print(f"DATABASE_URL do os.getenv: {os.getenv('DATABASE_URL', 'NÃO ENCONTRADA')}")
    print("-" * 50)
    
    db_type = detect_database_type()
    print(f"🔍 Testando {db_type}...")
    print("=" * 50)
    
    # Mostrar configuração atual
    db_url = os.getenv("DATABASE_URL", "sqlite:///./bloguide.db")
    print(f"📍 Banco configurado: {db_url}")
    print(f"🎯 Tipo detectado: {db_type}")
    print("-" * 50)
    
    # Executar testes
    if test_connection():
        if test_tables():
            test_basic_operations()
    else:
        print("❌ Verifique a configuração do banco de dados")
    
    print("=" * 50)
    print("✅ Teste concluído!")