import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_PATH = os.getenv("DB_PATH", "banco_dados.db")

# Em produção (Render), DATABASE_URL aponta pro Postgres gerenciado. Sem essa
# variável definida (dev local, ou enquanto o Postgres não é provisionado no
# Render), cai automaticamente pro arquivo SQLite de sempre.
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Render (e outros provedores) ainda entregam a URL no esquema antigo
# "postgres://", que o SQLAlchemy 1.4+ não aceita mais — precisa ser
# "postgresql://".
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
