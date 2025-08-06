import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv(".env", override=True)

class Settings:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "")

settings = Settings()
