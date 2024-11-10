import os

DB_USER = os.getenv("POSTGRES_USER") or "postgres"
DB_NAME = os.getenv("POSTGRES_DB") or "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD") or "change-me"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@db:5432/{DB_NAME}"
MAX_UNITIES = 20
AWESOME_URL = "https://cep.awesomeapi.com.br/json/"
DEBUG = os.getenv("DEBUG") == "True"
