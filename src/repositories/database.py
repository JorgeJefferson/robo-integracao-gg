from json import load
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv
import os


load_dotenv()


session_maker = sessionmaker(
    bind=create_engine(os.getenv("ROBO_INTEGRACAO_GG_DATABASE_URL", ""), echo=False),
)


@contextmanager
def get_session_context():
    """Retorna uma sessão do banco de dados."""
    session = session_maker()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    else:
        session.commit()
    finally:
        session.close()
