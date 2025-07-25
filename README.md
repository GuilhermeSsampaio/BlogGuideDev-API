# BlogGuide Backend API 🚀

API REST robusta construída com FastAPI para a plataforma BlogGuide - uma rede social focada em desenvolvedores.

## 📋 Sobre o Projeto

A API do BlogGuide fornece endpoints completos para:

- 🔐 **Autenticação JWT** - Login, registro e gerenciamento de sessões
- 👥 **Gerenciamento de Usuários** - CRUD completo com perfis públicos
- 📝 **Sistema de Posts** - Criação, listagem e gerenciamento de conteúdo
- 🏷️ **Sistema de Tags** - Categorização dinâmica de posts
- 🛡️ **Middleware de Segurança** - CORS, validação e tratamento de erros

## 🛠️ Tecnologias Utilizadas

### Core Framework

- **FastAPI 0.116.1** - Framework web moderno e rápido
- **SQLModel 0.0.24** - ORM baseado em Pydantic e SQLAlchemy
- **Uvicorn 0.35.0** - Servidor ASGI de alta performance

### Banco de Dados

- **SQLAlchemy 2.0.41** - ORM principal
- **PostgreSQL** - Produção (via psycopg2-binary)
- **SQLite** - Desenvolvimento local

### Autenticação & Segurança

- **python-jose 3.5.0** - JWT tokens
- **passlib 1.7.4** - Hash de senhas com bcrypt
- **python-multipart 0.0.20** - Upload de arquivos

### Utilitários

- **python-dotenv 1.1.1** - Gerenciamento de variáveis de ambiente
- **email-validator 2.2.0** - Validação de emails
- **sentry-sdk 2.33.0** - Monitoramento de erros

## 🏗️ Arquitetura da API

```
backend/
├── main.py                 # Aplicação principal FastAPI
├── database.py            # Configuração do banco de dados
├── requirements.txt       # Dependências Python
├── Dockerfile             # Container Docker
├── fly.toml              # Configuração Fly.io
├── generate-secret-key.py # Utilitário para gerar chaves
├── .env.example          # Template de variáveis
├── auth/
│   └── security.py       # Funções de segurança JWT
├── models/
│   ├── user.py           # Modelos de usuário
│   ├── post.py           # Modelos de post
│   └── auth.py           # Modelos de autenticação
├── routes/
│   ├── auth.py           # Endpoints de autenticação
│   ├── user.py           # Endpoints de usuários
│   ├── post.py           # Endpoints de posts
│   └── general.py        # Endpoints gerais
└── services/             # Serviços externos (futuro)
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- pip ou poetry
- PostgreSQL (produção) ou SQLite (desenvolvimento)

### Instalação Local

1. **Clone o repositório**

```bash
git clone <repository-url>
cd Bloguide/backend
```

2. **Crie ambiente virtual**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale dependências**

```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///./bloguide.db  # ou PostgreSQL URL
ENVIRONMENT=development
```

5. **Gere chave secreta (recomendado)**

```bash
python generate-secret-key.py
```

6. **Execute a aplicação**

```bash
# Desenvolvimento
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Ou usando Python
python main.py
```

7. **Acesse a documentação**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🐳 Docker

### Build da Imagem

```bash
docker build -t bloguide-api .
```

### Executar Container

```bash
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=your-db-url \
  bloguide-api
```

## 🌐 Deploy

### Fly.io (Configurado)

1. **Instalar Fly CLI**

```bash
# Instalar flyctl
curl -L https://fly.io/install.sh | sh
```

2. **Login e Deploy**

```bash
fly auth login
fly deploy
```

### Configurações de Produção

- **App Name**: `blogguidedev-api`
- **Region**: `gru` (São Paulo)
- **Memory**: 512MB
- **Health Check**: `/health`
- **Auto-scaling**: Habilitado

## 📚 Documentação da API

### Endpoints Principais

#### 🔐 Autenticação (`/auth`)

```http
POST /auth/register     # Registrar novo usuário
POST /auth/login        # Login do usuário
GET  /auth/me          # Obter usuário atual
POST /auth/logout      # Logout
```

#### 👥 Usuários (`/users`)

```http
GET    /users           # Listar usuários
GET    /users/{id}      # Obter usuário específico
POST   /users           # Criar usuário
PUT    /users/{id}      # Atualizar usuário
DELETE /users/{id}      # Deletar usuário
GET    /users/{id}/posts        # Posts do usuário
GET    /users/{username}/profile # Perfil público
```

#### 📝 Posts (`/posts`)

```http
GET    /posts           # Listar posts
GET    /posts/{id}      # Obter post específico
POST   /posts           # Criar post
DELETE /posts/{id}      # Deletar post
```

#### 🏥 Saúde (`/health`)

```http
GET    /health          # Status da API
```

### Modelos de Dados

#### User

```json
{
  "id": 1,
  "name": "João Silva",
  "username": "joao",
  "email": "joao@example.com",
  "bio": "Desenvolvedor Python",
  "github_url": "https://github.com/joao",
  "linkedin_url": "https://linkedin.com/in/joao",
  "avatar_url": "https://example.com/avatar.jpg",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": null
}
```

#### Post

```json
{
  "id": 1,
  "title": "Introdução ao FastAPI",
  "category": "Tutorial",
  "content": "FastAPI é um framework...",
  "author_id": 1,
  "image_url": "https://example.com/image.jpg",
  "tags": ["python", "fastapi", "tutorial"],
  "likes_count": 0,
  "is_published": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": null
}
```

## 🔒 Segurança

### JWT Authentication

- **Algoritmo**: HS256
- **Expiração**: 30 minutos
- **Header**: `Authorization: Bearer <token>`

### Middleware

- **CORS**: Configurado por ambiente
- **Validation**: Pydantic models
- **Error Handling**: HTTPException personalizado

### Ambiente de Produção

```python
# CORS restrito
origins = [
    "https://blog-guide-dev-front.vercel.app",
    "https://blogguidedev-api.fly.dev",
]
```

### Ambiente de Desenvolvimento

```python
# CORS amplo para testes
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

## 🗄️ Banco de Dados

### Modelos Principais

#### Users Table

```sql
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    bio VARCHAR(500),
    github_url VARCHAR(255),
    linkedin_url VARCHAR(255),
    avatar_url VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

#### Posts Table

```sql
CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES user(id),
    image_url VARCHAR(255),
    tags TEXT,  -- JSON string
    likes_count INTEGER DEFAULT 0,
    is_published BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

## 🧪 Desenvolvimento

### Scripts Úteis

```bash
# Desenvolvimento com auto-reload
uvicorn main:app --reload

# Gerar nova chave secreta
python generate-secret-key.py

# Verificar health
curl http://localhost:8000/health
```

### Variáveis de Ambiente

```env
SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///./bloguide.db
ENVIRONMENT=development
PORT=8000
```

## 🚨 Monitoramento

### Health Checks

- **Endpoint**: `/health`
- **Fly.io**: Verifica a cada 15s
- **Response**: `{"status": "healthy", "environment": "production"}`

### Logs

```bash
# Logs do Fly.io
fly logs

# Logs locais
tail -f logs/app.log
```

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'feat: adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

### Padrões de Código

- **PEP 8** para formatação
- **Type hints** obrigatório
- **Docstrings** para funções públicas
- **SQLModel** para modelos de dados

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Desenvolvedor

**Guilherme Sampaio**  
Dev Fundador

---

🚀 **API em Produção**: https://blogguidedev-api.fly.dev  
📖 **Documentação**: https://blogguidedev-api.fly.dev/docs

---

Feito com ❤️ para a comunidade de desenvolvedores (readme ainda em desenvolvimento)
