import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_PATH = os.getenv("DB_PATH", "banco_dados.db")
