import requests
import json

def test_register():
    """Testar registro com dados corretos"""
    print("👤 Testando registro corrigido...")
    
    user_data = {
        "name": "João Silva",
        "username": "joao12321",
        "email": "joao231@test.com",
        "password": "senha123",
        "bio": "Desenvolvedor Python"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Aceitar tanto 200 quanto 201 como sucesso
        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ Usuário registrado com sucesso!")
            print(f"  ID: {result.get('id')}")
            print(f"  Nome: {result.get('name')}")
            print(f"  Email: {result.get('email')}")
            print(f"  Username: {result.get('username')}")
            print(f"  Bio: {result.get('bio')}")
            print(f"  Ativo: {result.get('is_active')}")
            print(f"  Criado em: {result.get('created_at')}")
            return True
        else:
            print(f"❌ Erro no registro: {response.status_code}")
            if response.text:
                try:
                    error_detail = response.json().get('detail', 'Erro desconhecido')
                    print(f"  Detalhe: {error_detail}")
                except:
                    print(f"  Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: API não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_login():
    """Testar login com o usuário criado"""
    print("🔐 Testando login...")
    
    login_data = {
        "email": "joao@test.com",
        "password": "senha123"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login realizado com sucesso!")
            print(f"  Token Type: {result.get('token_type')}")
            print(f"  Access Token: {result.get('access_token')[:50]}...")
            print(f"  Usuário: {result.get('user', {}).get('name')}")
            return result.get('access_token')
        else:
            print(f"❌ Erro no login: {response.status_code}")
            if response.text:
                try:
                    error_detail = response.json().get('detail', 'Erro desconhecido')
                    print(f"  Detalhe: {error_detail}")
                except:
                    print(f"  Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro inesperado no login: {e}")
        return False

def test_duplicate_registration():
    """Testar registro duplicado (deve falhar)"""
    print("🔄 Testando registro duplicado...")
    
    user_data = {
        "name": "João Silva 2",
        "username": "joao456", 
        "email": "joao@test.com",  # Email já usado
        "password": "senha123",
        "bio": "Teste duplicação"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            error_detail = response.json().get('detail', 'Erro desconhecido')
            print("✅ Validação de duplicação funcionando!")
            print(f"  Erro esperado: {error_detail}")
            return True
        else:
            print(f"❌ Deveria ter retornado erro 400, mas retornou: {response.status_code}")
            print(f"  Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de duplicação: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testando sistema de autenticação completo...")
    print("=" * 60)
    
    # Teste 1: Registro
    register_success = test_register()
    print()
    
    # Teste 2: Login (se registro funcionou)
    if register_success:
        token = test_login()
        print()
        
        # Teste 3: Registro duplicado
        test_duplicate_registration()
    
    print("=" * 60)
    print("✅ Testes concluídos!")