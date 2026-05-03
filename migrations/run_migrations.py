import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def ensure_migration_table(connection):
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS migration_log (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    )


def get_applied_migrations(connection):
    rows = connection.execute(text("SELECT filename FROM migration_log")).fetchall()
    return {row[0] for row in rows}


def apply_migration(connection, migration_path: Path):
    sql = migration_path.read_text(encoding="utf-8").strip()
    if not sql:
        return

    connection.exec_driver_sql(sql)
    connection.execute(
        text("INSERT INTO migration_log (filename) VALUES (:filename)"),
        {"filename": migration_path.name},
    )


def main():
    load_dotenv()
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL não definido no ambiente")

    migrations_dir = Path(__file__).resolve().parent / "versions"
    if not migrations_dir.exists():
        raise RuntimeError(f"Diretório de migrations não encontrado: {migrations_dir}")

    engine = create_engine(database_url, pool_pre_ping=True)
    migration_files = sorted(migrations_dir.glob("*.sql"))

    with engine.begin() as connection:
        ensure_migration_table(connection)
        applied = get_applied_migrations(connection)

        pending = [m for m in migration_files if m.name not in applied]
        if not pending:
            print("Nenhuma migration pendente.")
            return

        for migration_file in pending:
            print(f"Aplicando migration: {migration_file.name}")
            apply_migration(connection, migration_file)

    print("Migrations aplicadas com sucesso.")


if __name__ == "__main__":
    main()
