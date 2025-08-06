import os
from dotenv import load_dotenv

# Carrega variáveis do .env do diretório atual
load_dotenv(os.path.join(os.getcwd(), ".env"), override=True)

class Settings:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "")

settings = Settings()
