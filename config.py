import os

############### Postgres Configuration ###############
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5438"))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PWD = os.getenv("POSTGRES_PWD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

