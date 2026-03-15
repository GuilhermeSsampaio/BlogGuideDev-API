from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Session
from config.db import create_db_and_tables, engine
from config.settings import API_TITLE, API_VERSION
from config.middlewares import setup_middlewares
from config.routers import setup_routers
from repository.conteudo_crud import create_conteudo_if_not_exists

CONTEUDOS_SEED = [
    ("html-css", "HTML e CSS"),
    ("javascript-jquery", "JavaScript e jQuery"),
    ("react", "React"),
    ("nextjs", "Next.js"),
    ("quasar", "Quasar Framework"),
    ("bootstrap", "Bootstrap"),
    ("vuejs", "Vue.js 3"),
    ("react-native-expo", "React Native e Expo"),
    ("angular", "Angular"),
    ("android-studio", "Android Studio"),
    ("flutter", "Flutter"),
    ("php", "PHP"),
    ("laravel", "Laravel"),
    ("python", "Python"),
    ("c-language", "C"),
    ("java", "Java"),
    ("nodejs-express", "Node.js e Express"),
    ("typescript", "TypeScript"),
    ("cobol", "COBOL"),
    ("docker", "Docker"),
    ("github-copilot", "GitHub Copilot"),
    ("git-github", "Git e GitHub"),
    ("framework-agno", "Framework Agno"),
    ("lovable-bolt", "Lovable e Bolt.new"),
    ("scrum-kanban", "Scrum e Kanban"),
    ("windows", "Windows"),
    ("linux", "Linux"),
    ("macos", "macOS para Desenvolvedores"),
    ("mysql-mongodb", "MySQL e MongoDB"),
    ("strapi-neondb", "Strapi e NeonDB"),
    ("oracle", "Oracle"),
    ("vercel", "Vercel"),
    ("render", "Render"),
    ("railway", "Railway"),
    ("flyio", "Fly.io"),
    ("aws", "Amazon Web Services (AWS)"),
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        for slug, titulo in CONTEUDOS_SEED:
            create_conteudo_if_not_exists(session, slug, titulo)
    yield


app = FastAPI(title=API_TITLE, version=API_VERSION, lifespan=lifespan)

setup_middlewares(app)
setup_routers(app)


@app.get("/")
async def root():
    return {"Bem vindo": "GuiSamp api"}


@app.get("/health")
async def health():
    return {"status": "ok"}
