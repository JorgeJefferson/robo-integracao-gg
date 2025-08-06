from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String


Base = declarative_base()


class CadUsuariosGEG(Base):
    __tablename__ = "cad_usuarios_geg"

    email_cad_usuarios_geg = Column(String, primary_key=True)
    senha_cad_usuarios_geg = Column(String, nullable=False)

    def __repr__(self):
        return f"<CadUsuariosGEG(email={self.email_cad_usuarios_geg})>"
