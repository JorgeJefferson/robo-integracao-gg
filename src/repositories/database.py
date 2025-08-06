from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config.settings import settings


session_maker = sessionmaker(
    bind=create_engine(settings.database_url, echo=False),
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
